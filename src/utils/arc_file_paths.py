def get_chs_name(stage_id):
    stage_id = int(stage_id)
    if int(stage_id) >= 100:
        return (str(stage_id - 100).zfill(2) + '_b').encode('utf-8')
    return str(stage_id).zfill(2).encode('utf-8')

def get_stage_preview(stage_id):
    return b'ui\\chs\\chs_stg\\chs_st_b\\chs_stg'+get_chs_name(stage_id)+b'_BM_HQ_NOMIP.241f5deb.tex'

def get_small_stage_preview(stage_id):
    return b'ui\\chs\\chs_stgt\\chs_st_m\\chs_stgm'+get_chs_name(stage_id)+b'_BM_HQ_NOMIP.241f5deb.tex'

def get_stage_text(stage_id):
    return b'ui\\chs\\chs_stgn\\chs_st_n\\chs_stgn'+get_chs_name(stage_id)+b'_BM_HQ_NOMIP.241f5deb.tex'

def get_stage_arcade_text(stage_id):
    return b'ui\\res\\res_stgm\\stgm_next_n\\res_stgn'+get_chs_name(stage_id)+b'_BM_HQ_NOMIP.241f5deb.tex'

def get_announcer(stage_id):
    stage_id = int(stage_id)
    path = b'sound\\se\\nar\\nar_chrsel\\source\\2na1_%se.724df879.rif'

    sound_map = {
        105: '118',
        5: '119',
        104: '120',
        4: '121',
        110: '122',
        10: '123',
        103: '124',
        3: '125',
        102: '126',
        2: '127',
        109: '128',
        9: '129',
        107: '130',
        7: '131',
        106: '132',
        6: '133',
        100: '134',
        0: '135',
        11: '136',
    }

    return path % (sound_map[stage_id].encode('utf-8'),)