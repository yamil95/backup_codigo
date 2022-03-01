data_scrap = pd.read_csv("scrap.csv")
data_maestro = pd.read_csv("maestro.csv")
data_scrap["marca_unidad"] = data_scrap["marca"]+ "" + data_scrap["presentacion"]
catNotMatched = data_scrap["marca_unidad"].to_list()
CatRaizen = list(data_maestro["item"])

# delete unnecesary simbols
simbols = re.compile('(?<=\s)x(?=\s)|[-_+?¿%$#!;*()"\']|(?<!\d)[.](?!\d)')
# join oil measure if it has white space (ej 20 W 40  --> 20W40)
oil = re.compile('(?<=\d)\s(?=w)|(?<=w)\s(?=\d)')

# regexs to normalize the unit of measurement
liters = re.compile('(?<=[\d\s,./]\d)\s?(litro|lit|ltr|lt|l)s?(?!\w)')
centil = re.compile('(?<=[\d\s,./]\d)\s?(c.c.|cc|cl)s?(?!\w)')

kilos = re.compile('(?<=[\d\s,./]\d)\s?(kilo|kil|kgr|kg|k)s?(?!\w)')
grams = re.compile('(?<=[\d\s,./]\d)\s?(gramo|grs|gr|g)s?(?!\w)')

meter = re.compile('(?<=[\d\s,./]\d)\s?(metro|mt|m)s?(?!\w)')
centim = re.compile('(?<=[\d\s,./]\d)\s?(centimetro|ctm|cm)s?(?!\w)')

# drop unnecesary whitespaces (<=2)
spaces = re.compile('\s{2,}')

# Regex to extract numbers and unit of measurement from str
units = re.compile('(\d|\d+[.,/]?\d+\s?)(\s--\w+--)')

def to_float(s: str):
    """
    Convert str to float and divide it if is necesary
    """
    try:
        return float(s)
    except ValueError as ex:
#         print(ex)
        if ',' in s:
            return float(s.replace(',', '.'))
        elif '/' in s:
            num, denom = s.split('/')
            return float(num) / float(denom)
        else:
            raise ex


def clean_col(column: pd.Series, drop_dupl=False):
    """
    Clean str columns applying previous regex
    """
    assert column.dtype.name == 'object', \
        'Columns must be type object (str)'

    clean_col = column.str.lower()\
                      .str.replace(simbols, '')\
                      .str.replace(oil, '')\
                      .str.replace(spaces, ' ')\
                      .str.replace(liters, ' --L--')\
                      .str.replace(centil, ' --C--')\
                      .str.replace(grams,  ' --G--')\
                      .str.replace(kilos,  ' --K--')\
                      .str.replace(centim, ' --N--')\
                      .str.replace(meter,  ' --M--')\
                      .str.replace(spaces, ' ')\
                      .str.strip()
    if drop_dupl:
        clean_col = clean_col.drop_duplicates()
    clean_col.name = 'description'
    return clean_col


def extract_units(column: pd.Series, normalize_units=False):
    """
    Extract measures from given col, and return as a df
    """
    assert column.dtype.name == 'object', \
        'Columns must be type object (str)'

    unit_col = column.str.extract(units)

    unit_col.rename(columns={0:'amount', 1: 'measure'}, inplace=True)
    unit_col.loc[:, 'amount'] = unit_col['amount'].map(to_float)

    unit_col.loc[:, 'measure'] = unit_col.measure.str.strip()
    if normalize_units:
        unit_col.loc[unit_col.measure == '--C--', 'amount'] /= 1000  # cc to liters
        unit_col.loc[unit_col.measure == '--C--', 'measure'] = '--L--'
        unit_col.loc[unit_col.measure == '--G--', 'amount'] /= 1000  # gr to kilos
        unit_col.loc[unit_col.measure == '--G--', 'measure'] = '--K--'
        unit_col.loc[unit_col.measure == '--N--', 'amount'] /= 1000  # cm to meter
        unit_col.loc[unit_col.measure == '--N--', 'measure'] = '--M--'

    return pd.concat([column, unit_col], axis=1)
	
	
eess_descr = clean_col(df_cat.marca, drop_dupl=True).dropna().values
raizen_descr = clean_col(pd_DIM_Articulos.item, drop_dupl=True).dropna().values

len(eess_descr), len(raizen_descr)

def match_words(word: str, bag_of_words: List[str]):
    """
    Compare word with all bag_of_words and return closer string usign rapidfuzz.token_set_ratio as measure
    """
    
    def similar(a, b):
        return SequenceMatcher(None, a, b).real_quick_ratio()
  
    # token_set_ratio with str2 seted
    token_ratio = partial(fuzz.token_set_ratio, s2=word)
    
    # vectorize map token_set_ratio over each token on bag_of_words
    results = np.vectorize(token_ratio)(bag_of_words)
    best_match, score = bag_of_words[np.argmax(results)], results[np.argmax(results)]
    return {'s1': word,
            's2': best_match,
            'score': score,
            'similar': similar(word, best_match),
           }
		   
# partial functions with bag_of_words
match_words_part = partial(match_words, bag_of_words=raizen_descr)

# comparte all eess description vs all raizen description
with Pool(os.cpu_count()) as procces:
        results = procces.map(match_words_part, eess_descr)
		
		
threshold = 90
df_wuzzy = pd.DataFrame(results)
df_wuzzy.rename(columns={'s1': 'cat', 's2': 'art'}, inplace=True)


df_cat.loc[:, 'clean_descr'] = clean_col(df_cat.marca)
pd_DIM_Articulos.loc[:, 'clean_item'] = clean_col(pd_DIM_Articulos.item)

eess_cols = ['id','marca','nombre', 'presentacion','clean_descr']
raizen_cols = ['item', 'coditem', 'clean_item']


dfFuzzPandas = df_wuzzy[(df_wuzzy.score >= threshold) & (df_wuzzy.similar > .6)].copy()

dfFuzzPandas = pd.merge(dfFuzzPandas, df_cat[eess_cols],
                          how='left', left_on='cat', right_on='clean_descr')
dfFuzzPandas = pd.merge(dfFuzzPandas, pd_DIM_Articulos[raizen_cols],
                          how='left', left_on='art', right_on='clean_item')
						  
						  
dfExcepciones = df_wuzzy[(df_wuzzy.score < threshold)].copy()

dfExcepciones = pd.merge(dfExcepciones, df_cat[eess_cols],
                          how='left', left_on='cat', right_on='clean_descr')
dfExcepciones = pd.merge(dfExcepciones, pd_DIM_Articulos[raizen_cols],
                          how='left', left_on='art', right_on='clean_item')
						  
						  

# ------------------------------------------------------------------------- #
# TOMA LOS KEY / VALOR QUE HAYAN DADO MAYOR SCORE Y SE ELIMINAN LOS REPETIDOS 
# ------------------------------------------------------------------------- #

dfFuzzPandas = dfFuzzPandas.sort_values(by='score', ascending=False)
dfExcepciones = dfExcepciones.sort_values(by='score', ascending=False)



# ---------------------------------- #
# CREA UNA VISTA DEL PAR KEY / VALOR
# ---------------------------------- #

dfFuzzy = spark.createDataFrame(dfFuzzPandas)
dfFuzzy.createOrReplaceTempView( "dfFuzzy" )

dfEx = spark.createDataFrame(dfExcepciones)
dfEx.createOrReplaceTempView( "dfEx" )


