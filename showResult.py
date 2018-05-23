#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
import os
 
label_dic={"LOC_S":0,"LOC_B":0, "LOC_I":0, "LOC_E":0}
pred_dic={"LOC_S":0,"LOC_B":0, "LOC_I":0, "LOC_E":0}
corr_dic={"LOC_S":0,"LOC_B":0, "LOC_I":0, "LOC_E":0}

if __name__=="__main__":
    file = open(os.path.join(os.path.dirname(__file__),'test.rst'))

    wc = wc_loc = 0
    wc_of_test = 0
    wc_of_gold = 0
    wc_of_correct = 0
    flag = True
    
    for line in file:
        line=line.strip()
        if len(line)==0:continue

        _,_,label,pred=line.strip().split()
        wc += 1
        if "LOC" not in label and "LOC" not in pred: continue #
        wc_loc+=1
        if 'LOC' in label: label_dic[label]+=1
        if 'LOC' in pred:   pred_dic[pred]+=1
        if label==pred: corr_dic[label]+=1

 
    print "Word count:", wc
    print "Word_loc count:", wc_loc
    print "真实位置标记个数：", label_dic
    print "预估位置标记个数：",pred_dic
    print "正确标记个数：", corr_dic

    res ={"LOC_S":0.0,"LOC_B":0.0, "LOC_I":0.0, "LOC_E":0.0}

    all_gold = 0
    all_correct = 0
    all_pre = 0
    for k in label_dic:
        print "------ %s -------"%(k)
        R = corr_dic[k]/float(label_dic[k])  #召回率
        P = corr_dic[k]/float(pred_dic[k])   #准确率
        print "[%s] P = %f, R = %f, F-score = %f" % (k,P, R, (2*P*R)/(P+R))

        all_pre += pred_dic[k]
        all_correct += corr_dic[k]
        all_gold += label_dic[k]
    print "------ All -------"
    all_R = all_correct/float(all_gold)
    all_P = all_correct/float(all_pre)
    print "[%s] P = %f, R = %f, F-score = %f" % ("All",all_P, all_R, (2*all_P*all_R)/(all_P+all_R))



# WordCount from result: 220612
# WordCount of loc_wc  post : 5791
# 真实位置标记个数： {'LOC_E': 197, 'LOC_B': 197, 'LOC_S': 5262, 'LOC_I': 95}
# 预估位置标记个数： {'LOC_E': 149, 'LOC_B': 137, 'LOC_S': 5303, 'LOC_I': 57}
# 正确标记个数： {'LOC_E': 124, 'LOC_B': 107, 'LOC_S': 5233, 'LOC_I': 42}
# ------ LOC_E -------
# [LOC_E] P = 0.832215, R = 0.629442, F-score = 0.716763
# ------ LOC_B -------
# [LOC_B] P = 0.781022, R = 0.543147, F-score = 0.640719
# ------ LOC_S -------
# [LOC_S] P = 0.986800, R = 0.994489, F-score = 0.990629 单字识别F值最高
# ------ LOC_I -------
# [LOC_I] P = 0.736842, R = 0.442105, F-score = 0.552632
# ------ All -------
# [All] P = 0.975204, R = 0.957399, F-score = 0.966219
    

