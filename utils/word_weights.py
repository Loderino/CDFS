import pymorphy3

morph = pymorphy3.MorphAnalyzer()

def get_tag_weight(tag):
    if " " in tag:
        words = tag.split()
        weights = [get_word_weight(word) for word in words]
        # Берем среднее и добавляем бонус за словосочетание
        return sum(weights)/len(weights) + 0.5  # Увеличенный бонус для словосочетаний
    else:
        return get_word_weight(tag)

def get_word_weight(word):
    parsed = morph.parse(word)[0]
    pos = parsed.tag.POS
    
    weights = {
        # Ключевые объекты и концепты
        'NOUN': 2.0,  # Существительные (основа большинства запросов)
        
        # Важные характеристики
        'ADJF': 1.2,  # Прилагательные полные
        'ADJS': 1.2,  # Прилагательные краткие
        'NUMR': 1.5,  # Числительные (важны для точных запросов)
        
        # Действия
        'VERB': 1.3,  # Глаголы
        'INFN': 1.3,  # Инфинитивы
        'PRTF': 1.1,  # Причастия полные
        'PRTS': 1.1,  # Причастия краткие
        'GRND': 1.0,  # Деепричастия
        
        # Вспомогательные части речи
        'ADVB': 0.8,  # Наречия
        'NPRO': 0.7,  # Местоимения-существительные
        'PREP': 0.4,  # Предлоги
        'CONJ': 0.3,  # Союзы
        'PRCL': 0.3,  # Частицы
        'INTJ': 0.5,  # Междометия
    }
    
    # Дополнительные модификаторы
    if 'anim' in parsed.tag and pos == 'NOUN':
        weights[pos] += 3.5  # Одушевленные существительные значительно важнее
    
    if 'Name' in parsed.tag or 'Surn' in parsed.tag:
        weights[pos] += 1.0  # Имена и фамилии важнее обычных существительных
    
    if 'Geox' in parsed.tag:
        weights[pos] += 0.8  # Географические названия важнее обычных существительных
    
    return weights.get(pos, 1.0)  # Для неизвестных частей речи вес 1.0
