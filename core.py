from random import randint


class Feature:
    def __init__(self,
                 weight_HP=0.0, weight_DEF=0.0, weight_ATK=0.0, weight_Element_Mastery=0.0,
                 weight_HP_Rate=0.0, weight_DEF_Rate=0.0, weight_ATK_Rate=0.0,
                 weight_Energy_Recharge=0.0, weight_CRIT_Rate=0.0, weight_CRIT_DMG=0.0,):
        self.category = ['HP', 'DEF', 'ATK', 'Element_Mastery', 'HP_Rate', 'DEF_Rate', 'ATK_Rate', 'Energy_Recharge',
                         'CRIT_Rate', 'CRIT_DMG']
        self.upgrade_range = [['HP', 209, 299],
                              ['DEF', 16, 23],
                              ['ATK', 14, 19],
                              ['Element_Mastery', 16, 23],
                              ['HP_Rate', 4.1, 5.8],
                              ['DEF_Rate', 5.1, 7.3],
                              ['ATK_Rate', 4.1, 5.8],
                              ['Energy_Recharge', 4.5, 6.5],
                              ['CRIT_Rate', 2.7, 3.9],
                              ['CRIT_DMG', 5.4, 7.8]]  # range that value can increase in an upgrade due to the feature
        self.weights = [['HP', 0.026 * weight_HP],
                        ['DEF', 0.335 * weight_DEF],
                        ['ATK', 0.398 * weight_ATK],
                        ['Element_Mastery', 0.33 * weight_Element_Mastery],
                        ['HP_Rate', 1.33 * weight_HP_Rate],
                        ['DEF_Rate', 1.33 * weight_DEF_Rate],
                        ['ATK_Rate', 1.33 * weight_ATK_Rate],
                        ['Energy_Recharge', 1.1979 * weight_Energy_Recharge],
                        ['CRIT_Rate', 2 * weight_CRIT_Rate],
                        ['CRIT_DMG', 1 * weight_CRIT_DMG]]  # the features weight when count the score

    def upgrade_value(self, feature_name):
        for i in self.upgrade_range:
            if i[0] == feature_name:
                a = int(i[1] * 10)
                b = int(i[2] * 10)
                return randint(a, b)/10
        return


class SYW:
    def __init__(self,
                 feature_main, level,
                 feature_1, feature_2, feature_3, feature_4,  # features are string
                 value_1, value_2, value_3, value_4):
        self.feature_main = feature_main
        self.level = level
        self.features = [feature_1, feature_2, feature_3, feature_4]
        self.values = [value_1, value_2, value_3, value_4]

    def distribution(self, feature, simulation_times=10000):
        sorted_score = self.estimate(feature, simulation_times)
        mean_score = 0
        for i in sorted_score:
            mean_score += i
        mean_score = mean_score/simulation_times
        sorted_score.sort()
        start = int(sorted_score[0]*10)/10
        end = int(sorted_score[-1]*10)/10
        axis_range = int((end - start) * 10 + 1)
        list_1 = [0]*axis_range
        list_2 = [0]*axis_range
        list_3 = [0]*axis_range
        axis = start
        for i in range(axis_range):
            list_3[i] = axis
            axis += 0.1
        list_1_value = simulation_times
        current_index = 0
        axis = start
        for i in range(axis_range):
            list_2_value = 0
            for j in range(simulation_times - current_index):
                if sorted_score[current_index+j] < axis:
                    list_2_value += 1
                else:
                    break
            axis += 0.1
            current_index += list_2_value
            list_2[i] = list_2_value/simulation_times*10
            list_1_value -= list_2_value
            list_1[i] = list_1_value/simulation_times
        return list_1, list_2, list_3, mean_score  # list_1 is the curve of probability, list_2 is the distribution of the probability

    def estimate(self, feature, simulation_times=10000):
        score_list = [0]*simulation_times
        for i in range(simulation_times):
            copy_syw = self.copy()
            score_list[i] = copy_syw.up_full_level(feature)
        return score_list

    def copy(self):
        copy_object = SYW(self.feature_main, self.level,
                          self.features[0], self.features[1], self.features[2], self.features[3],
                          self.values[0], self.values[1], self.values[2], self.values[3])
        return copy_object

    def up_full_level(self, feature):
        upgrade_times = int((23 - self.level) / 4)
        upgrade_times = self.begin_with_three(feature, upgrade_times)
        for i in range(upgrade_times):
            self.upgrade(feature)
        return self.score(feature)

    def begin_with_three(self, feature, times):
        upgrade_times = times
        for i in self.features:
            if i is None:
                category = feature.category[:]
                self.features.remove(None)
                exceptions = self.features[:]
                exceptions.append(self.feature_main)
                for e in exceptions:
                    category.remove(e)
                new_feature = category[randint(0,5)]
                self.features.append(new_feature)
                self.values[3] = self.values[3] + feature.upgrade_value(self.features[3])
                upgrade_times = upgrade_times - 1
                break
        return upgrade_times

    def upgrade(self, feature):
        random_feature = randint(0, 3)
        self.values[random_feature] = self.values[random_feature] + feature.upgrade_value(self.features[random_feature])

    def score(self, feature):
        score = 0
        for i in range(4):
            for weight in feature.weights:
                if weight[0] == self.features[i]:
                    score = score + self.values[i] * weight[1]
        return score

    def show_inform(self):
        print(self.features)
        print(self.values)

def smooth(list, avg=3):
    for i in range(len(list)-avg+1):
        res = 0
        for j in range(avg):
            res += list[i+j]
        list[i+int(avg/2)] = res/avg






