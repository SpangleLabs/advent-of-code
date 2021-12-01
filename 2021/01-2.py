my_input = """100
101
105
106
103
104
106
108
112
123
125
149
158
147
150
153
156
166
171
172
174
186
193
198
203
217
220
235
239
242
245
243
237
238
246
247
238
242
254
256
263
261
281
287
296
300
317
318
338
342
345
346
344
349
355
372
386
393
394
382
384
398
405
420
433
426
427
431
446
447
450
454
455
454
460
451
453
454
433
436
437
425
433
434
443
445
454
455
461
462
465
478
480
492
501
512
530
528
519
520
522
529
534
542
555
567
565
566
568
569
582
596
597
606
610
611
618
619
632
633
634
635
647
650
655
658
659
661
701
713
715
719
720
729
722
758
765
774
791
796
800
804
807
810
819
823
824
828
833
837
838
835
843
844
845
844
850
856
859
863
883
885
886
907
937
938
941
958
959
960
962
963
964
966
967
973
977
979
981
975
978
980
977
978
983
984
972
973
969
970
974
989
1001
1002
1003
1029
1035
1038
1042
1045
1072
1075
1076
1078
1090
1099
1103
1099
1111
1116
1117
1120
1115
1131
1152
1155
1166
1179
1187
1188
1191
1185
1190
1192
1193
1194
1200
1182
1199
1202
1185
1186
1194
1191
1218
1225
1218
1228
1238
1240
1241
1243
1258
1275
1283
1284
1288
1285
1286
1287
1295
1296
1295
1296
1302
1304
1307
1336
1337
1340
1345
1346
1361
1362
1368
1365
1371
1382
1384
1388
1400
1401
1412
1415
1432
1435
1443
1455
1464
1489
1484
1488
1493
1496
1497
1499
1503
1502
1517
1518
1519
1548
1573
1576
1577
1580
1583
1590
1591
1590
1595
1602
1604
1603
1604
1607
1608
1612
1613
1614
1617
1597
1606
1607
1606
1615
1616
1617
1621
1624
1623
1624
1622
1625
1626
1630
1640
1641
1644
1648
1645
1649
1650
1651
1658
1660
1668
1658
1659
1694
1695
1697
1700
1713
1722
1724
1727
1738
1739
1737
1764
1765
1762
1767
1771
1772
1776
1779
1789
1807
1809
1830
1836
1839
1841
1861
1871
1873
1878
1879
1880
1883
1890
1900
1908
1909
1912
1909
1910
1920
1926
1932
1930
1931
1936
1938
1941
1951
1943
1948
1926
1933
1947
1944
1950
1970
1971
1981
1982
1984
1986
1991
2011
2010
2024
2026
2028
2029
2030
2044
2046
2073
2074
2075
2090
2088
2092
2093
2094
2102
2117
2118
2139
2137
2139
2143
2139
2143
2147
2149
2150
2152
2148
2149
2150
2151
2153
2157
2154
2159
2157
2140
2142
2157
2163
2174
2175
2180
2191
2198
2197
2199
2197
2201
2204
2217
2219
2223
2222
2238
2257
2258
2257
2265
2272
2290
2296
2297
2303
2307
2309
2310
2311
2327
2328
2325
2337
2336
2344
2354
2355
2356
2345
2356
2360
2361
2360
2361
2362
2378
2407
2403
2408
2409
2415
2421
2414
2415
2416
2429
2431
2442
2450
2453
2460
2490
2497
2498
2503
2494
2496
2505
2509
2519
2520
2528
2540
2545
2544
2563
2568
2571
2577
2593
2599
2604
2606
2617
2634
2635
2636
2642
2617
2618
2627
2634
2635
2615
2624
2625
2620
2612
2610
2612
2614
2616
2619
2622
2618
2620
2630
2642
2644
2645
2646
2647
2622
2623
2626
2624
2634
2638
2648
2647
2646
2647
2648
2657
2664
2665
2671
2664
2666
2677
2707
2720
2724
2725
2727
2736
2739
2741
2747
2762
2764
2767
2766
2761
2762
2763
2767
2768
2776
2783
2785
2771
2780
2781
2795
2801
2803
2814
2822
2841
2860
2869
2877
2882
2907
2908
2938
2943
2944
2945
2973
2977
2997
3002
2998
3001
3003
3004
3015
3014
3019
3022
3028
3029
3030
3031
3033
3032
3036
3042
3043
3042
3055
3076
3077
3091
3088
3077
3081
3086
3087
3095
3101
3121
3123
3124
3125
3132
3133
3149
3150
3151
3166
3186
3187
3191
3192
3195
3203
3204
3205
3206
3208
3209
3211
3236
3224
3236
3231
3267
3271
3272
3273
3275
3283
3284
3291
3315
3325
3337
3338
3345
3348
3358
3367
3366
3365
3372
3374
3376
3377
3385
3388
3405
3411
3432
3437
3435
3457
3462
3470
3475
3482
3487
3492
3491
3492
3501
3507
3513
3508
3513
3523
3533
3535
3571
3575
3586
3587
3591
3605
3604
3612
3614
3615
3620
3625
3640
3658
3660
3674
3680
3681
3682
3687
3688
3690
3692
3699
3700
3703
3728
3734
3738
3766
3767
3775
3782
3786
3794
3798
3799
3806
3831
3832
3837
3838
3845
3854
3887
3888
3899
3901
3911
3912
3918
3919
3920
3921
3937
3940
3947
3948
3960
3961
3962
3976
3931
3933
3934
3948
3950
3958
3944
3948
3957
3963
3968
3969
3986
3994
4018
4029
4035
4040
4048
4061
4066
4072
4080
4087
4094
4086
4084
4090
4099
4105
4106
4107
4102
4116
4119
4130
4131
4150
4163
4176
4192
4189
4199
4209
4210
4211
4220
4223
4266
4257
4258
4259
4260
4255
4256
4257
4283
4305
4306
4307
4315
4317
4326
4323
4331
4343
4337
4344
4350
4372
4373
4369
4377
4378
4355
4356
4357
4365
4366
4368
4383
4384
4385
4388
4380
4389
4397
4413
4417
4422
4434
4442
4445
4447
4451
4452
4461
4464
4466
4467
4468
4492
4498
4505
4510
4511
4509
4510
4517
4516
4527
4523
4524
4527
4533
4534
4535
4543
4553
4554
4556
4557
4566
4544
4546
4552
4575
4576
4581
4584
4585
4591
4581
4582
4584
4595
4596
4597
4584
4586
4594
4604
4610
4646
4662
4663
4671
4698
4711
4716
4719
4739
4743
4745
4743
4747
4751
4762
4765
4772
4791
4801
4804
4811
4826
4827
4828
4831
4850
4851
4852
4853
4855
4863
4875
4895
4901
4902
4907
4926
4928
4929
4933
4969
5004
5011
5015
5017
5019
5021
5019
5024
5026
5029
5033
5036
5054
5060
5064
5068
5051
5052
5053
5058
5059
5060
5068
5069
5081
5083
5086
5090
5091
5093
5094
5112
5114
5126
5129
5146
5149
5151
5159
5161
5162
5138
5154
5166
5174
5188
5189
5192
5194
5209
5213
5214
5216
5225
5227
5240
5241
5242
5237
5269
5270
5286
5291
5293
5294
5295
5301
5302
5304
5299
5332
5333
5339
5344
5350
5363
5365
5370
5393
5385
5390
5393
5401
5404
5405
5415
5418
5421
5422
5423
5427
5428
5444
5448
5450
5457
5438
5464
5466
5469
5486
5489
5492
5494
5495
5491
5504
5505
5511
5512
5535
5537
5546
5547
5565
5568
5570
5560
5567
5576
5587
5588
5606
5608
5611
5642
5643
5651
5656
5665
5666
5667
5672
5679
5688
5695
5700
5704
5705
5701
5705
5706
5705
5710
5716
5711
5717
5720
5709
5717
5719
5720
5723
5724
5725
5732
5729
5730
5743
5756
5757
5756
5758
5761
5762
5765
5766
5795
5800
5802
5804
5811
5818
5823
5832
5841
5845
5837
5824
5825
5830
5847
5855
5856
5859
5860
5867
5868
5872
5870
5858
5865
5866
5879
5889
5890
5901
5902
5903
5913
5915
5920
5925
5936
5938
5939
5940
5952
5950
5955
5964
5969
5964
5975
5976
5984
6006
6007
6009
6013
6023
6025
6027
6030
6031
6033
6066
6067
6068
6070
6072
6078
6082
6078
6121
6147
6157
6161
6193
6194
6197
6198
6204
6206
6207
6209
6219
6232
6243
6251
6253
6251
6252
6254
6255
6254
6263
6264
6267
6268
6260
6267
6273
6289
6294
6295
6298
6334
6336
6353
6354
6366
6375
6380
6420
6428
6429
6430
6431
6441
6455
6460
6451
6481
6482
6503
6506
6524
6526
6546
6550
6555
6564
6566
6565
6570
6568
6569
6570
6580
6604
6616
6623
6626
6627
6633
6645
6646
6664
6682
6676
6694
6699
6704
6708
6710
6701
6710
6714
6733
6737
6760
6773
6774
6775
6785
6772
6794
6807
6796
6794
6803
6804
6807
6806
6809
6843
6855
6869
6883
6894
6912
6920
6929
6928
6926
6940
6943
6947
6946
6949
6950
6981
6982
7000
7001
7006
7027
7028
7030
7054
7071
7075
7093
7085
7094
7097
7098
7101
7102
7101
7108
7132
7131
7132
7143
7148
7151
7154
7151
7161
7167
7181
7188
7189
7191
7197
7198
7200
7215
7224
7250
7254
7262
7277
7287
7289
7292
7294
7295
7296
7297
7298
7316
7317
7329
7332
7333
7336
7343
7342
7343
7348
7350
7355
7353
7355
7357
7354
7370
7391
7392
7401
7408
7414
7420
7424
7435
7409
7411
7412
7424
7442
7443
7445
7447
7451
7453
7475
7486
7489
7497
7498
7499
7500
7515
7505
7507
7532
7530
7531
7535
7549
7550
7568
7569
7570
7589
7590
7586
7589
7590
7591
7602
7608
7612
7613
7626
7621
7624
7625
7638
7639
7642
7643
7651
7655
7623
7628
7622
7610
7611
7635
7645
7653
7656
7659
7663
7666
7682
7687
7688
7683
7705
7707
7710
7714
7707
7710
7714
7715
7716
7705
7708
7709
7710
7715
7719
7731
7733
7715
7718
7731
7753
7747
7745
7729
7731
7732
7734
7735
7755
7758
7757
7758
7776
7794
7798
7802
7803
7805
7807
7814
7838
7839
7856
7862
7857
7860
7869
7871
7872
7874
7899
7914
7924
7916
7894
7893
7891
7892
7902
7901
7913
7919
7920
7934
7935
7940
7931
7941
7946
7957
7951
7952
7951
7966
7967
7968
7969
7975
8013
8021
8040
8043
8044
8057
8059
8068
8069
8078
8079
8086
8089
8107
8109
8110
8113
8105
8111
8112
8111
8116
8119
8128
8135
8136
8139
8140
8145
8146
8157
8160
8162
8163
8172
8183
8201
8209
8214
8220
8216
8219
8214
8216
8222
8226
8217
8226
8245
8246
8260
8265
8266
8262
8265
8266
8250
8247
8250
8245
8248
8252
8253
8255
8257
8259
8270
8287
8299
8300
8313
8316
8327
8337
8339
8356
8363
8384
8396
8399
8413
8419
8420
8432
8445
8440
8430
8442
8445
8446
8466
8467
8469
8466
8468
8469
8476
8484
8488
8503
8518
8542
8543
8554
8559
8561
8558
8579
8574
8570
8571
8572
8576
8577
8581
8576
8578
8602
8603
8606
8608
8605
8606
8610
8615
8639
8652
8666
8670
8678
8689
8690
8691
8692
8712
8714
8725
8726
8734
8737
8739
8740
8733
8726
8728
8716
8718
8736
8738
8742
8743
8761
8769
8772
8802
8825
8831
8836
8841
8846
8848
8849
8850
8856
8854
8862
8863
8869
8872
8877
8882
8888
8893
8892
8891
8893
8894
8900
8918
8921
8928
8927
8928
8931
8932
8940
8942
8950
8954
8955
8958
8962
8976
8978
8980
8981
8986
8987
8997
9005
9007
9009
9020
9024
9053
9056
9092
9111
9112
9114
9122
9133
9123
9126
9138
9113
9119
9121
9122
9121
9122
9123
9124
9125
9120
9136
9137
9126
9133
9137
9138
9141
9143
9145
9146
9147
9160
9153
9154
9153
9166
9181
9182
9189
9194
9195
9196
9197
9210
9215
9225
9236
9239
9242
9244
9245
9249
9248
9257
9256
9253
9255
9267
9269
9271
9275
9276
9290
9310
9312
9333
9338
9342
9343
9367
9387
9411
9412
9423
9436
9451
9458
9459
9461
9466
9468
9467
9475
9477
9481
9483
9480
9487
9502
9519
9526
9535
9533
9536
9537
9531
9530
9535
9540
9542
9555
9560
9566
9568
9563
9574
9575
9576
9577
9578
9581
9583
9584
9583
9582
9600
9603
9615
9619
9622
9640
9648
9627
9633
9634
9659
9666
9667
9670
9673
9693
9692
9694
9695
9688
9701
9702
9703
9705
9706
9707
9712
9702
9703
9712
9713
9718
9735
9736
9739
9741
9744
9747
9759
9760
9762
9763
9764
9767
9771
9774
9775
9777
9785
9786
9787
9789
9810
9818
9825
9830
9844
9846
9848
9858
9862
9876
9879
9906
9905
9906
9907
9909
9914
9913
9915
9920
9921
9934
9940
9946
9955
9958
9960
9968
9970
9971
9983
10002
10001
10013
10014
10015
10009
10021
10022
10045
10038
10049
10050
10083
10103
10101
10107
10103
10104
10107
10125
10120
10121
10120
10122
10124
10139
10145
10146
10138
10151
10152
10153
10161
10163
10166
10169
10172
10176
10190
10191
10194
10195
10189
10197
10203
10209
10227
10219
10222
10224
10233
10246
10236
10237
10238
10239
10268
10269
10273
10272
10284"""

increases = 0
lines = my_input.split("\n")
window = [int(x) for x in lines[:3]]
prev_line = int(lines[0])
for line in lines[3:]:
    cur_line = int(line)
    new_window = window[1:] + [cur_line]
    if sum(new_window) > sum(window):
        increases += 1
    window = new_window
print(increases)
