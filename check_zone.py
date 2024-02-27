"""KNT21617 KD.TRONG - CHECKING 08:00:00 - 15/12/2023"""
import pandas as pd

def condition_zone(dict_zone, data_df):
    list_synonym = [["usa", "us"], ["canada", "can"]]
    key_fumon = ""
    for key in dict_zone.keys():
        if key == "usa":
            key = "us"
        if key == "canada":
            key = "can"
        if len(key_fumon) == 0:
            key_fumon = key
        else:
            key_fumon = key_fumon + "_" + key

    Dict_return = {}
    flg_check, list_other = check_other(data_df)
    all_check, list_all = check_all(data_df)
    fumon_check, list_fumon = check_fumon(data_df)
    if all_check:
        Dict_return.update({key: list_all for key in dict_zone.keys()})
        for key_all in Dict_return.keys():
            if key_all == 'us':
                matching_columns = data_df.columns[
                    data_df.iloc[1].apply(lambda x: str(x).lower().replace('rus', '').strip()).str.contains(
                        key_all)].tolist()
            else:
                matching_columns = data_df.columns[
                    data_df.iloc[1].apply(lambda x: str(x).lower()).str.contains(key_all)].tolist()
            if len(matching_columns) > 0:
                x = Dict_return[key_all].copy()
                x.extend([[i, data_df.loc[2, i]] if data_df.loc[2, i] in ["最下級", "最上級"] else [i, "不問"] for i in
                     matching_columns])
                Dict_return[key_all] = x
                break
            else:
                None
    elif fumon_check:
        Dict_return.update({key_fumon: list_fumon})
    else:
        for key in dict_zone.keys():
            key_symstr = symstr(key, list_synonym)
            for item in key_symstr:
                if item == 'us':
                    matching_columns = data_df.columns[
                        data_df.iloc[1].apply(lambda x: str(x).lower().replace('rus', '').strip()).str.contains(
                            item)].tolist()
                else:
                    matching_columns = data_df.columns[
                        data_df.iloc[1].apply(lambda x: str(x).lower()).str.contains(item)].tolist()
                if len(matching_columns) > 0:
                    Dict_return[item] = [
                        [i, data_df.loc[2, i]] if data_df.loc[2, i] in ["最下級",
                                                                        "最上級"] else [i,
                                                                                        "不問"]
                        for i in matching_columns
                    ]
                    break
                else:
                    None
            if len(matching_columns) == 0 and flg_check:
                Dict_return[item] = list_other
            elif len(matching_columns) == 0 and not flg_check:
                Dict_return[item] = []
    return fumon_check, Dict_return, all_check


"""
Name function: create_zone_dataframe
Create dataframe for "zone"
input: data_karenhyo2
ouput: result_df (dataframe):  DataFrame containing only the "zone" column.
"""

def create_zone_dataframe(data_karenhyo2):
    data_karenhyo2 = data_karenhyo2.map(lambda x: x.lower() if isinstance(x, str) else x)
    data_test = data_karenhyo2.iloc[1:4, 11:]
    data_test = data_test.reset_index(drop=True)
    result_df = data_test.copy().loc[:, data_test.loc[0] == 'zone']
    # print(result_df)
    return result_df


"""
Name function: symstr
Create dataframe for "zone"
input: 
    zone:  Zone is specified
    list_synonym: List all of market are same meaning.
ouput: [zone] (List) List market are same meaning.
"""


def symstr(zone, list_synonym):
    for item in list_synonym:
        if zone in item:
            return item
    return [zone]


"""
Name function: check_other
Check the existence of "other".
input: 
    list_synonym:  List of names for other cases.
    data_karenhyo2: DataFrame containing only the "zone" column.
ouput: 
    other_check(bool): True or False 
    list_other(List): results 
"""
def check_other(data_df):
    list_synonym = ["other", "その他"]
    list_other = []
    other_check = True
    list_other_columns = []
    try:
        for item in list_synonym:
            list_other_columns = data_df.columns[
                data_df.iloc[1].apply(lambda x: str(x).lower()).str.contains(item)].tolist()
            if len(list_other_columns) > 0:
                other_check = True
                list_other = [
                    [i, data_df.loc[2, i]] if data_df.loc[2, i] in ["最上級", "最下級"] else [i, "不問"] for i
                    in list_other_columns]
                break
        if len(list_other_columns) == 0:
            other_check = False
            list_other = []
        return other_check, list_other
    except:
        return False,[]


"""
Name function: check_all
Check the existence of "all".
input: 
    data_karenhyo2: DataFrame containing only the "zone" column.
ouput: 
    all_check(bool): True or False 
    list_all(List): results
"""


def check_all(data_karenhyo2):
    all_check = False
    list_all = []
    try:
        all_columns = data_karenhyo2.columns[
            data_karenhyo2.iloc[1].apply(lambda x: str(x).lower()).str.contains('all')].tolist()
        if len(all_columns) > 0:
            all_check = True
            list_all = [[i, data_karenhyo2.loc[2, i]] if data_karenhyo2.loc[2, i] in ["最上級", "最下級"] else [i, "不問"]
                        for i in all_columns]
        return all_check, list_all
    except:
        return False, []


"""
Name function: check_fumon
Check the existence of "fumon" or "-" or blank.
input: 
    data_karenhyo2: DataFrame containing only the "zone" column.
ouput: 
    all_check(bool): True or False 
    list_all(List): results
"""
def check_fumon(data_karenhyo2):
    fumon_check = False
    list_fumon = []
    try:
        fumon_columns = data_karenhyo2.columns[
            data_karenhyo2.iloc[1].apply(lambda x: str(x).lower()).str.contains('不問|-|nan|ー')].tolist()
        if len(fumon_columns) > 0:
            fumon_check = True
            list_fumon = [
                [i, data_karenhyo2.loc[2, i]] if data_karenhyo2.loc[2, i] in ["最下級", "最上級"] else [i, "不問"]
                for i in fumon_columns
            ]

        return fumon_check, list_fumon
    except:
        return False, []

def dict_detect(dict_1):
    dic_ref = dict_1.copy()
    for key in dic_ref.keys():
        if key == "canada":
            dict_1["can"] = dict_1.pop("canada")
        if key == "usa":
            dict_1["us"] = dict_1.pop("usa")

    dict_result = {}
    elements_list = []
    for key, value in dict_1.items():
        elements_list.extend(value)

    unique_list = []

    for item in elements_list:
        if item not in unique_list:
            unique_list.append(item)

    for y in unique_list:
        found_keys = []
        for key, value in dict_1.items():
            if y in value:
                found_keys.append(key)

        if found_keys:
            key_combine = f"{'_'.join(found_keys)}"
            if key_combine not in dict_result.keys():
                dict_result[key_combine] = [y]
            else:
                if isinstance(y, list):
                    dict_result[key_combine].append(y)
                else:
                    dict_result[key_combine].append([y])

        else:
            None
    return dict_result


def condition_zone_check(data_karenhyo2, dict_zone):
    data_df = create_zone_dataframe(data_karenhyo2)
    fumon_check, Dict_return, all_check = condition_zone(dict_zone, data_df)
    if all_check:
        end_dict = Dict_return
    else:
        end_dict = dict_detect(Dict_return)
    return all_check,end_dict

