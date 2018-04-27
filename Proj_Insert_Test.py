#!/usr/bin/python
# -*- coding: UTF-8 -*-

#This is cross_project insert MySQL program
#Writen by LS in 2017_11_14


import string
import re
import shutil
import collections
import logging
import pymysql.cursors
import sys
import os


def headersClassify(fblock): #[(index,release时间,项目名称，文件名称，src，start,end),(****),****]
	headers_infos = []
	data = open(fblock,'r')
	for line in data:
		header_tmp = line.split(",")
		if(len(header_tmp) == 4):
			index = header_tmp[0]
			proj_src = header_tmp[1]
			start_line = header_tmp[2]
			end_line = header_tmp[3]
		else:
			index = header_tmp[0]
			proj_src = header_tmp[1] + "," + header_tmp[2]
			start_line = header_tmp[3]
			end_line = header_tmp[4]
		proj_src_tmp = proj_src.split("/")
		keywords = proj_src_tmp[7]
		pos = proj_src_tmp.index(keywords)
		proj_pos = proj_src_tmp[pos+1:]
		headers_info = (int(index),keywords,proj_pos[0],proj_pos[-1],proj_src,int(start_line),int(end_line))
		headers_infos.append(headers_info)

	return headers_infos


def PairInfos(Detection_Block, pairfile, headers_infos, block_infos) :
	Detection_Id = int(Detection_Block[0][0])
	Detection_TP = str(Detection_Block[0][1])

	clonepair_id = 0
	data = open(pairfile,'r')
	clonepairinfos = []
	for line in data:
		block1, block2 = line.split(",")
		if(headers_infos[int(block1)][1] == headers_infos[int(block2)][1]):
			pairinfo=(Detection_Id, Detection_TP, int(clonepair_id), int(block1), int(block2), int(block_infos[int(block1)][3]), int(block_infos[int(block1)][4]), int(block_infos[int(block2)][3]), int(block_infos[int(block2)][4]),int(0))
		else:
			pairinfo=(Detection_Id, Detection_TP, int(clonepair_id), int(block1), int(block2), int(block_infos[int(block1)][3]), int(block_infos[int(block1)][4]), int(block_infos[int(block2)][3]), int(block_infos[int(block2)][4]), int(1))
		clonepairinfos.append(pairinfo)
		clonepair_id = clonepair_id + 1
	return clonepairinfos

		


def DetectionInfos(fdetection):
	data = open(fdetection,'r')

	Detection_Block = []
	line = []
	for i in data:
		s = i.strip('\n')
		line.append(s)

	detection_info = (int(line[0]), str(line[1]), float(line[2]), line[3], line[4], int(line[5]), line[6])
	Detection_Block.append(detection_info)

	return Detection_Block


def RepositoryInfos(Detection_Block):
	Detection_Id = int(Detection_Block[0][0])
	Detection_TP = str(Detection_Block[0][1])
	repository_dir = "/mnt/winE/SourcererCC/clone-detector/input/dataset"
	repository_infos = []
	count = 0
	repository_id = 0
	release_id = 0
	repository_files = os.listdir(repository_dir)
	for name in repository_files:
		release_id = 0
		repository_name=os.path.splitext(name)
		release_dir = "/mnt/winE/SourcererCC/clone-detector/input/dataset/"+repository_name[0]+repository_name[1]
		release_files = os.listdir(release_dir)
		for release in release_files:
			release_name=os.path.splitext(release)
			repository_info = (int(Detection_Id), Detection_TP,int(repository_id),int(release_id),str(repository_name[0]+repository_name[1]),str(release_name[0]+release_name[1]))
			repository_infos.append(repository_info)
			release_id = release_id + 1
			count = count + 1
		repository_id = repository_id + 1
	return repository_infos


def BlockInfos(repository_infos, fblock):
	Detection_Id = int(repository_infos[0][0])
	Detection_TP = str(repository_infos[0][1])
	block_infos = []
	data = open(fblock,'r')
	for line in data:
		header_tmp = line.split(",")
		if len(header_tmp) == 4:
			block_id = header_tmp[0]
			block_src = header_tmp[1]
			start_line = header_tmp[2]
			end_line = header_tmp[3]
		else:
			block_id = header_tmp[0]
			block_src = header_tmp[1] + "," + header_tmp[2]
			start_line = header_tmp[3]
			end_line = header_tmp[4]
		block_src_tmp = block_src.split("/")
		project_name = block_src_tmp[7]
		release_name = block_src_tmp[8]
		repository_id = 0
		release_id = 0
		codefile = open(block_src,"rb")
		codeList = codefile.readlines()[int(start_line)-1:int(end_line)]
		codeString = str(codeList)
		for i in range(len(repository_infos)):
			if repository_infos[i][4] == project_name and repository_infos[i][5] == release_name:
				repository_id = repository_infos[i][2]
				release_id = repository_infos[i][3]
		block_info = (Detection_Id, Detection_TP, int(block_id), int(repository_id), int(release_id), block_src_tmp[-1], block_src, int(start_line), int(end_line), int(int(end_line) - int(start_line)) + 1, codeString)
		block_infos.append(block_info)
	return block_infos



def tokenclones(fpair):
	data = open(fpair,'r')
	clonepairs = []
	for line in data:
		block1, block2 = line.split(",")
		clonepairs.append((int(block1), int(block2), 0))
	return clonepairs


def toEasyDict(clonepairs):
	def  by_one(t):
		return t[0]
	clones = sorted(clonepairs,key = by_one)
	idict = collections.OrderedDict()
	for pair in clones:
		idict[pair[0]] = idict.get(pair[0],[False,[]])
		idict[pair[0]][1].append(pair[1])
	for k,v in idict.items():
		v[1].sort()
	return idict


def PairToLink(clonepairs):
	result = []
	def recur(key):
		value = clonepairs.get(key,-1)
		if value != -1 and not value[0]:
			for member in value[1]:
				s.add(member)
				recur(member)
			value[0] = True	
	for k,v in clonepairs.items():
		if not v[0]:
			s = set([])
			s.add(k)
			recur(k)
			result.append(sorted(list(s)))	
	return result
	

def GroupInstance(Detection_Block,result):
	Detection_Id = int(Detection_Block[0][0])
	Detection_TP = str(Detection_Block[0][1])
	count = 0
	group_instance_infos = []
	for cloneList in result:
		Group_idlist = ','.join(str(x) for x in cloneList)
		for x in cloneList:
			group_instance_info = (int(Detection_Id), Detection_TP, int(count), int(x))
			group_instance_infos.append(group_instance_info)
		count = count + 1
	return group_instance_infos


def Groupinfos(Detection_Block, result):
	Detection_Id = int(Detection_Block[0][0])
	Detection_TP = str(Detection_Block[0][1])
	count = 0
	group_infos = []
	for cloneList in result:
		Group_idlist = ','.join(str(x) for x in cloneList)
		group_info = (int(Detection_Id), Detection_TP, int(count), Group_idlist)
		group_infos.append(group_info)
		count = count + 1
	return group_infos

def CProjectInfos(irepository_infos):
	project_infos = []
	for a,b,c,d,e,f in irepository_infos:
		project_info = (int(a), b,int(c),int(d),str(e),str(f),int(-1),int(-1))
		project_infos.append(project_info)
	return project_infos


def ProjectInfos(iconn,irepository_infos):
	cursor = iconn.cursor()
	project_infos = []
	#release_foreignkey = -1
	#repository_foreignkey = -1
	for a,b,c,d,e,f in irepository_infos:
		ef_str = "%"+e+"/"+f+"%"
		sql = """SELECT * FROM gitrelease WHERE src_address LIKE %s"""
		try:
			cursor.execute(sql,(ef_str))
			data = cursor.fetchall()
		except:
			print("Error: unable to fetch data")
		for row in data:
			for key in row:
				if key == "git_release_id":
					release_foreignkey = row[key]
				if key == "repository_id":
					repository_foreignkey = row[key]
		project_info = (int(a), b,int(c),int(d),str(e),str(f),int(release_foreignkey),int(repository_foreignkey))
		project_infos.append(project_info)
	iconn.close()
	return project_infos

def TokenInfos(Detection_Block, filename):

	Detection_Id = int(Detection_Block[0][0])
	Detection_TP = str(Detection_Block[0][1])

	token_infos = []
	fp = open(filename,"r")
	for line in fp:
		frequency = []
		if line == '\n':
			continue
		
		token = line.split('@#@')

		block_id = token[0].split(',')[1]
		token_single = token[1].split(',')
		token_count = len(token_single)
		token_total = 0
		for i in range(token_count):
			word = re.split('@@::@@|\n',token_single[i])
			if len(word) >= 2 :
				frequency.append((word[0],word[1]))
				token_total = token_total + int(word[1])

		frequency = sorted(frequency, key= lambda x: x[0])
		frequency = sorted(frequency, key= lambda x: x[1], reverse=True)

		if len(frequency) < 1:
			continue
		token_string = frequency[0][0]
		token_frequency = frequency[0][0] + ',' + frequency[0][1]
		for i in range(1,len(frequency)):
			token_string = token_string + ',' + frequency[i][0]
			token_frequency = token_frequency + ';' + frequency[i][0] + ',' + frequency[i][1]
		token_info = (int(Detection_Id), Detection_TP,int(block_id),int(token_count),str(token_string),int(token_total),str(token_frequency))
		token_infos.append(token_info)

	#print(token_infos)
	return token_infos


