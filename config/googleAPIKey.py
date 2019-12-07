import os

jsonkey = '{"t<p#": "s#rv$c#_!cc&>nt", "pr&j#ct_$d": "#l$t#-cr&ssb!r-261208", "pr$v!t#_k#<_$d": "!987!6!420b15030f1#bd71510!d0!!817d1f#7#", "pr$v!t#_k#<": "-----BEGIN PRIVATE KEY-----HIHIHAHAMIIEvgIBADANBgkqhk$G9w0BAQEFAASCBKgwggSkAgEAA&IBAQDd$EjZ4CJFIFM2HIHIHAHAFC5b5gS/5!NfRIOc<YN<KhPtMk8m!PsE1MT2sdmhDVQrc/FXV6MGnx3Mm05hFPMhHIHIHAHAHkCcFHTSw$0Qrncb#W>19OEzE9#Q3+Md423+srmBhBYVdhNHD&Y0lU!s7YEkU9bSHIHIHAHAYAg+p&kEZAlYdkc63x$nb#13+zDBtq<fKM1Ll8YqODKmLUQG&DOFmkRwRP5xZq#kHIHIHAHAEkvM>xR3VB2zh2XEwj$P8qwkr/pKP<4<K0Cs5X2A4bq!FqXWzQsEF6G&+z8Oz84NHIHIHAHA+z&$fc>wZ88PW3lvBhcY<8N87UKIMEcH&zRWqzALHAVQzH5P$N4!Av>hFWT6P&DrHIHIHAHA<UMb&lLfAgMBAAECggEAKj+L+TU0A+/$vq0BnFgVLs2qJw$H#x!5QUQCEdnm22HpHIHIHAHAAWZc#9m2M#87TqApd$lJ94DP643w2DXpGjdNRhbm&q0ScBx9rZkt8AEYE6gkk8YGHIHIHAHA59PQT#M$2q7&kUY37fS4pn2TgXY4C0gL74&N+HjFJ7#2S&8gDX>vlXq<749R&J#NHIHIHAHAms/M2&MGWEwVlhlWHAFLW#rfTXWw8rN&r/NIY4fjDqw#N/x#fBO4dGmz$FIC5PRsHIHIHAHAI>5FXfLc>2pIcFwZxUHGELr!9vU08/jxDG#AtOTIn+C8bqxfvWIG7O+N6nSHtwCxHIHIHAHAtWT7tEcZxV<CFP+9!ZSBE2zsr8LE<pWw!j9BJr2qKQKBgQD1lm3/j0Q$xB8XF#7&HIHIHAHA!9f7gsTR467qREO#k!dLQsL5/TmJJv<UgUsqLWt3LPV2m#6$cZLYYjNZC&28HI$nHIHIHAHAA&nbSTwr8vMxV8<IR>sKtLQQZpbQk0&/pl>2R>ERTTsG7lMDsP0m#XOgO6+!rZCjHIHIHAHA09bqpWHRF4>cL/&qvz>wVCP5NwKBgQDm7MNKTb!0Y#!PMYOId>YYbDtf>A91sgzqHIHIHAHAq<qhCH!SEAWG<vsx7n1IPr36ZcznO/KCUrq1m8qdggNWUPlKRNqGVGU4$KY&1HqcHIHIHAHA+X1v>bTZb2&vr3OVkhrk!6$U6qvj1+B21vzglRJS2vBtWfY$Ct!nAZmdt3C5FUOMHIHIHAHATNxR+60nmQKBgQC!mWAV$PKzkBK$TcRf>8PzKJcOK#5q>x52K+rMjfJ/vNEDb#+CHIHIHAHA7QGMQ5trInpDdxOqX<S54tfALc<bprq/p/Fwg#HHKOG/J$4z#7Fqw+!2jF5UX>RWHIHIHAHAvTr>vB/$7GNEMbNAl6JFHh+Ttv8M>EZdW3XnsMSrA893Ox<Y3FmO3>jmcQKBgQCWHIHIHAHAvR6NtkT5Yp66Ajw2LEb>0l#/l8qfrWY5GRp>m7OqjMLOxllKsr8dFb#1!BZlKwCWHIHIHAHA$!JPQ$70>hWrlpfkH<X2YcjhKnIsXObc6Q80$<$+drf+AK2W$RT83jnhW35w8E4ZHIHIHAHAxSS1BR&886XV+89rUV/lDGpWRZRTfMnnH5UB/<N8&QKBgAV3cChmh>L3+A1Y/#&mHIHIHAHAYNO3JJOZmUrA$>M3mI9C8AQY9YsE9PIg9Hsv206tVIBMTw$GPDEV&qXGkmngXbEwHIHIHAHAUrXl27URB/YPmt3vEsSdmSX2Cz!b3TltIx/1BH#K$Dn4KvvSFnU<#&x>CP&4BVJPHIHIHAHADE<$H2UDb7kQqKBf5B8>/5D$HIHIHAHA-----END PRIVATE KEY-----HIHIHAHA", "cl$#nt_#m!$l": "f#-cr#d$t@#l$t#-cr&ssb!r-261208.$!m.gs#rv$c#!cc&>nt.c&m", "cl$#nt_$d": "100323979763703638912", "!>th_>r$": "https://!cc&>nts.g&&gl#.c&m/&/&!>th2/!>th", "t&k#n_>r$": "https://&!>th2.g&&gl#!p$s.c&m/t&k#n", "!>th_pr&v$d#r_x509_c#rt_>rl": "https://www.g&&gl#!p$s.c&m/&!>th2/v1/c#rts", "cl$#nt_x509_c#rt_>rl": "https://www.g&&gl#!p$s.c&m/r&b&t/v1/m#t!d!t!/x509/f#-cr#d$t%40#l$t#-cr&ssb!r-261208.$!m.gs#rv$c#!cc&>nt.c&m"}'

def writeKey():
  a = ['a', 'e', 'i', 'o', 'u', 'y']
  b = ['!', '#', '$', '&', '>', '<']
  res = jsonkey
  for i in range(len(a)):
      res = res.replace(b[i], a[i])
  res = res.replace('HIHIHAHA', '\\n')
  f = open(os.getcwd() + '/config/google api key.json', 'w')
  f.write(res)

def closeKey():
  f = open(os.getcwd() + '/config/google api key.json', 'w')
  f.write('')