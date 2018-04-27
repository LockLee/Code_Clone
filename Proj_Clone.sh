#! /bin/bash
# -*- coding: UTF-8 -*-

#This is project code clone SourcererCC program
#Writen by LS in 2017_11_8


Detection_ID=1
Detection_TP="#*--20180131"
Detection_Granularity="Functions"
Detection_Percent=0.90
Detection_Description="ID 1: Use SourcererCC Detection Method,Detection Time Piece is from begin to 20180131,Detection Granularity Is Function,Detection Similarity Threshold Is 0.90"


function SourcererCC(){

        Detection_ID=$1
        Detection_TP=$2
	Detection_Percent=$3
        Detection_Granularity=$4
        Detection_Description=$5


        ##修改目录权限
        cd /mnt/winE/SourcererCC/clone-detector/input
        chmod -R 777 ./dataset


        cd /mnt/winE/SourcererCC/clone-detector/parser/java
        ##程序运行日期时间
        RUN_DATE=`date`
        ##程序第一部分运行开始时间
        START1=$(date +%s)
        java -jar InputBuilderClassic.jar /mnt/winE/SourcererCC/clone-detector/input/dataset /mnt/winE/SourcererCC/clone-detector/input/query/tokens.file /mnt/winE/SourcererCC/clone-detector/input/bookkeping/headers.file functions java 0 0 10 0 false false false 8
        ##程序第一部分运行结束时间
        END1=$(date +%s)
        ##计算程序第一部分运行时间
        RUN_TIME1=$(( $END1 - $START1 ))

        ##同上  
        cd /mnt/winE/SourcererCC/clone-detector
        START2=$(date +%s)
        java -jar dist/indexbased.SearchManager.jar index 9
        END2=$(date +%s)
        RUN_TIME2=$(( $END2 - $START2 ))
        ##同上  
        cd /mnt/winE/SourcererCC/clone-detector
        START3=$(date +%s)
        java -jar dist/indexbased.SearchManager.jar search 9
        END3=$(date +%s)
        RUN_TIME3=$(( $END3 - $START3 ))

        #程序总运行时间
        RUN_TIME=$(( $RUN_TIME1 + $RUN_TIME2 + $RUN_TIME3))


        ##新建一个保存Detection信息的文件
        touch Detection.txt

        #echo 'The detection file path:'
        #pwd

        ##将Detection信息重定向到文件
        echo $Detection_ID >> Detection.txt
        echo $Detection_TP >> Detection.txt
        echo $Detection_Percent >> Detection.txt
	echo $Detection_Granularity >> Detection.txt
        echo $RUN_DATE >> Detection.txt
        echo $RUN_TIME >> Detection.txt
	echo $Detection_Description >> Detection.txt
}

SourcererCC $Detection_ID $Detection_TP $Detection_Percent $Detection_Granularity "$Detection_Description"
