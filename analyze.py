import pandas as pd
import numpy as np
file = 'data.xlsx'
df = pd.read_excel(file)

# 피험자 번호 리스트 생성
subject_ids = [f"A{str(i).zfill(2)}" for i in range(1, 44)] + [f"B{str(i).zfill(2)}" for i in range(1, 47)] + [f"C{str(i).zfill(2)}" for i in range(1, 72)] + [f"D{str(i).zfill(2)}" for i in range(1, 50)]


# 요일별, 체중 유형별, 피험자 번호별로 아침 식사를 하지 않은 비율을 계산하는 함수
def calculate_no_meal_rate(df, meal):
    results = {}
    days = ['월', '화', '수', '목', '금', '토', '일']
    weight_types = ['저체중', '표준체중', '과체중']

    for weight_type in weight_types:
        cnt = 0
        totalCnt = 0
        df2 = df[df['체중유형']==weight_type]
        print(len(df2))
        for day in days:
            for subject_id in subject_ids:
                #피험자가 해당 체중 유형에 해당할 때만 카운트
                if len(df2[df2['피험자번호'] == subject_id]) == 0:
                    continue
                totalCnt += 1
                # 해당 날짜, 체중 유형, 피험자 번호에 해당하는 데이터 필터링
                subject_df = df[(df['요일'] == day) & (df['체중유형'] == weight_type) & (df['피험자번호'] == subject_id)]
                # 아침 식사를 하지 않은 경우 카운트
                if not any(subject_df['식사유형'] == meal):
                    cnt += 1
        # 피험자가 없는 경우를 고려
        rate = cnt / totalCnt if totalCnt > 0 else 0
        results[weight_type] = rate * 100
        print(cnt, totalCnt, weight_type)
            
    return results

def calculate_no_meal_stats(df, meal):
    results = {}
    stats = {}
    days = ['월', '화', '수', '목', '금', '토', '일']
    weight_types = ['저체중', '표준체중', '과체중']

    for weight_type in weight_types:
        rates = []  # 각 체중 유형별 비율을 저장할 리스트
        for day in days:
            for subject_id in subject_ids:
                df_weight = df[df['체중유형'] == weight_type]
                if len(df_weight[df_weight['피험자번호'] == subject_id]) == 0:
                    continue
                subject_df = df[(df['요일'] == day) & (df['체중유형'] == weight_type) & (df['피험자번호'] == subject_id)]
                # 특정 식사를 하지 않은 경우 비율 계산
                if not any(subject_df['식사유형'] == meal):
                    rates.append(1)
                else:
                    rates.append(0)

        # 평균 및 표준 편차 계산
        mean_rate = np.mean(rates) * 100
        std_dev = np.std(rates) * 100
        results[weight_type] = mean_rate
        stats[weight_type] = {'mean': mean_rate, 'std_dev': std_dev}

    return stats


def rate(df, meal):
    results = {}
    days = ['월', '화', '수', '목', '금', '토', '일']
    weight_types = ['저체중', '표준체중', '과체중']

    for weight_type in weight_types:
        cnt = 0
        totalCnt = 0
        df2 = df[df['체중유형']==weight_type]
        print(len(df2))
        for day in days:
            for subject_id in subject_ids:
                #피험자가 해당 체중 유형에 해당할 때만 카운트
                if len(df2[df2['피험자번호'] == subject_id]) == 0:
                    continue
                totalCnt += 1
                # 해당 날짜, 체중 유형, 피험자 번호에 해당하는 데이터 필터링
                subject_df = df[(df['요일'] == day) & (df['체중유형'] == weight_type) & (df['피험자번호'] == subject_id)]
                # 음주, 야식을 하지 않은 경우 카운트
                if not any(subject_df['식사유형'] == meal):
                    cnt += 1
        # 피험자가 없는 경우를 고려
        rate = cnt / totalCnt if totalCnt > 0 else 0
        results[weight_type] = 100 - rate * 100
        print(cnt, totalCnt, weight_type)
            
    return results


import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

def plot_no_meal_rate(results, meal):
    weight_types = list(results.keys())
    no_breakfast_rates = [results[weight_type] for weight_type in weight_types]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(weight_types, no_breakfast_rates, color='gray')

    # x축, y축 레이블과 제목의 스타일 업데이트
    plt.xlabel('체중 유형', fontsize=12, labelpad = 15)
    plt.ylabel(meal+ ' 식사 결식률 (단위: %)', fontsize=12)
    plt.ylim(0, 100)  # 결식률은 0%에서 100% 사이의 값

    # 막대 위에 실제 값을 표시
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f"{yval:.2f}", ha='center', va='bottom', color='black', fontsize=12)

    # plt.show()
    plt.savefig(meal+'식사결식률.png')


# 함수 실행
no_breakfast_rate_results = calculate_no_meal_rate(df, '아침')
no_lunch_rate_results = calculate_no_meal_rate(df, '점심')
no_dinner_breakfast_rate_results = calculate_no_meal_rate(df, '저녁')

# no_breakfast_rate_results = calculate_no_meal_stats(df, '아침')
# no_lunch_rate_results = calculate_no_meal_stats(df, '점심')
# no_dinner_breakfast_rate_results = calculate_no_meal_stats(df, '저녁')

# print(no_breakfast_rate_results)
# print(no_lunch_rate_results)
# print(no_dinner_breakfast_rate_results)

# 그래프 그리기
plot_no_meal_rate(no_breakfast_rate_results, '아침')
plot_no_meal_rate(no_lunch_rate_results, '점심')
plot_no_meal_rate(no_dinner_breakfast_rate_results, '저녁')


# addi = rate(df, '음주')
# print(addi)
# plot_no_meal_rate(addi, '음주')
