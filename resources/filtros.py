

def normalize_path_params(cidade=None,
                          estrelas_min=0,
                          estrelas_max = 5,
                          diaria_min=0,
                          diaria_max=10000,
                          limit=50,
                          offset=0,**dados):
    if cidade:
        return{
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset
        }
        
    return{
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset
    }  
    
def consulta_sem_cidade(estrelas_min, estrelas_max, 
                        diaria_min, diaria_max, limit, offset):
    query = f"""SELECT * FROM hoteis
                       WHERE (estrelas >= {estrelas_min} and estrelas <= {estrelas_max})
                       and (diaria >= {diaria_min} and diaria <= {diaria_max})
                       LIMIT {limit} OFFSET {offset}
                       """
    return query

def consulta_com_cidade(estrelas_min, estrelas_max, diaria_min, diaria_max, cidade, limit, offset):
         
    query = f"""SELECT * FROM hoteis
                        WHERE 
                        (estrelas >= {estrelas_min} and estrelas <= {estrelas_max})
                        and (diaria >= {diaria_min} and diaria <= {diaria_max})
                        and cidade like '%{cidade}%' LIMIT {limit} OFFSET {offset}
                        """
    return query