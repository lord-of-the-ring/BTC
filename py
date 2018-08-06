# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 14:17:39 2018

@author: jason
"""

import math
import hashlib
def reduce_fraction(num, den):
    tmp_num = num
    tmp_den = den
    if(tmp_num < tmp_den):
        (tmp_num,tmp_den) = (tmp_den,tmp_num)
    while(tmp_num%tmp_den != 0):
        (tmp_num,tmp_den) = (tmp_den,tmp_num%tmp_den)
        #tmp_cc = tmp_num%tmp_den
        #tmp_num = tmp_den
        #tmp_den = tmp_cc
    return (int(num/tmp_den),int(den/tmp_den));
def pow_mod(a,b,c):   #快速幂算法
    a=a%c
    ans=1
    #这里我们不需要考虑b<0，因为分数没有取模运算
    while b!=0:
        if b&1:
            ans=(ans*a)%c
        b>>=1
        a=(a*a)%c
    return ans
#起点,网上csdn
G=(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
#
#G=(48439561293906451759052585252797914202762949526041747995844080717082404635286, 36134250956749795798585127919587881956611106672985015071877198253568414405109)
k = 0x1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD#csdn
#k = 0x18E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725#网上例子
#k = 0x1801280ab12039
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
p = 115792089237316195423570985008687907853269984665640564039457584007908834671663#这是csdn上的例子，我下面要用我的例子了
#p = 115792089210356248762697446949407573530086143415290314195533631308867097853951#github上面的
x_want = 0xF028892BAD7ED57D2FB57BF33081D5CFCF6F9ED3D3D7F159C2E2FFF579DC341A
y_want = 0x07CF33DA18BD734C600B96A72BBC4749D5141C90EC8AC328AE52DDFE2E505BDB

#print(k,'\n')
bk1= bin(k);
#print(bin(k)," ",len(bin(k))-2,'\n')
tmp = hex(13)
#print(tmp,'\n')
tmp = bin(0xd)
#print(tmp,'\n',len(tmp)-2)

itr = len(bin(k))-2;
print(itr,'\n')


x1 = G[0]
y1 = G[1]
x2 = G[0]
y2 = G[1]

#k = 7;
while (1):
    if(k&1):
        break
    (num,den) = (3*x2**2,2*y2)
    lemda1 = num%p
    lemda2 = pow_mod(den,p-2,p);
    lemda = (lemda1*lemda2)%p
    x3 = (lemda**2-2*x2)%p;
    y3 = (lemda*(x2-x3)-y2)%p;
    x2 = x3;
    y2 = y3;
    k>>1;
bk= bin(k);
for i in range(len(bin(k))-2, 1,-1):#最后再加上一位，先假设最后一位是1
    #print(i)
    #(num,den) = reduce_fraction(3*x2**2,2*y2)
    #(3*x2^2)/(2*y2)
    (num,den) = (3*x2**2,2*y2)
    #print(3*x2**2/num-2*y2/den)
    #for j in range(1,p):
     #   if((p*j+1)%den == 0):
     #       break;
    #den = (p*j+1)/den;
    #我现在要算的是(num *den^(g-2)) mod p
    #计算的是次幂
    lemda1 = num%p
    lemda2 = pow_mod(den,p-2,p);
    lemda = (lemda1*lemda2)%p
    #print(lemda)
    x3 = (lemda**2-2*x2)%p;
    y3 = (lemda*(x2-x3)-y2)%p;
    x2 = x3;
    y2 = y3;
    #判断是否加上次幂
    if(bk[i] == "1"):
        #print(i,end="")
        #(y2-y1)/(x2-x1)
        lemda1 = (y2-y1)%p;
        lemda2 = pow_mod(x2-x1,p-2,p);
        lemda = (lemda1*lemda2)%p;
        x3 = (lemda**2-x1-x2)%p;
        y3 = (lemda*(x1-x3)-y1)%p;
        #x3 = lemda**2-x1-x2;
        #y3 = lemda*(x1-x3)-y1;
        x1 = x3;
        y1 = y3;
#gg = len(str(bin(x1)))-2
print("未拼接y的x公钥长度",len(str(bin(x1)))-2,'\n')
#x_net = 0x04a34b99f22c790c4e36b2b3c2c35a36db06226e41c692fc82b8b56ac1c540c5bd5b8dec5235a0fa8722476c7709c02559e3aa73aa03918ba2d492eea75abea235

if(str(bin(y1)) == '0'):
    com_prefix= "02"
    compressed = "00000010"+str(bin(x1))[2:]
else:
    com_prefix= "03"
    compressed = "00000011"+str(bin(x1))[2:]
compressed = compressed[0:33*4]
print(compressed," ",len(compressed))

compressed_hex = ""
for i in range(0,33):
    compressed_hex+=(hex(int('0b'+compressed[i*4:i*4+4],2))[2:]) 
    print(hex(int('0b'+compressed[i*4:i*4+4],2))[2:],end="")
    #print(bk[i],end="")
print("压缩",com_prefix+hex(x1)[2:],"压缩")
# print((x1 ** 3 + 7 - y1**2)%p == 0)
 #print((x_want ** 3 + 7 - y_want**2)%p)
#compressed = "beyongjie" 
#print(address,len(address),"nihao") 
print('\n')
x1_hex = hex(x1)[2:].zfill(64)
y1_hex = hex(y1)[2:].zfill(64)
un_compressed = "04"+x1_hex+y1_hex
print(un_compressed,"未压缩公钥")
#un_compressed = "5c79cce6ad92b7b1da3eb9d8364070509d55f533c68bea3a0551e8da2a742f69fd5768e42b9f0a92b88240e92baf1cf5ef4de6bea28da877aa0205539dd4105b"
#un_compressed =  "0010"
address_mine = hashlib.sha256(un_compressed.encode('utf-8')).hexdigest()
#address_mine = hashlib.sha256(un_compressed).hexdigest()
print(address_mine,"hash256")
#address_mine = 0xa44962e777eaa5c397e2cd38ae8ec02381e797de16b7e94313d2b4e02f9021a1
address = 0x600FFE422B4E00731A59557A5CCA46CC183944191006324A447BDB2D98D4B408
address_bin = bin(address)[2:]
ripmed = hashlib.new('ripemd160', address_mine.encode('utf-8')).hexdigest()
print(ripmed,len(ripmed),"ripmed-160")
 #以下为私钥转地址的程序
 
