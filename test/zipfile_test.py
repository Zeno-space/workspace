# # import zipfile

# # z = zipfile.ZipFile('a.zip','w')
# # z.write('shopping_cart_count')
# # print(help(z.write))
# # z.close()
# #以上写法不能遍历目录
# #以下似乎很复杂，python2



# def zip_dir(dirname,zipfilename):
#     filelist = []
#     if os.path.isfile(dirname):
#         filelist.append(dirname)
#     else :
#         for root, dirs, files in os.walk(dirname):
#             for dir in dirs:
#                 filelist.append(os.path.join(root,dir))
#             for name in files:
#                 filelist.append(os.path.join(root, name))

#     zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
#     for tar in filelist:
#         arcname = tar[len(dirname):]
#         #print arcname
#         zf.write(tar,arcname)
#     zf.close()

# def unzip_dir(zipfilename, unzipdirname):  
#     fullzipfilename = os.path.abspath(zipfilename)  
#     fullunzipdirname = os.path.abspath(unzipdirname)  
#     print（"Start to unzip file %s to folder %s ..." % (zipfilename, unzipdirname)  
#     #Check input ...  
#     if not os.path.exists(fullzipfilename):  
#         print "Dir/File %s is not exist, Press any key to quit..." % fullzipfilename  
#         inputStr = raw_input()  
#         return  
#     if not os.path.exists(fullunzipdirname):  
#         os.mkdir(fullunzipdirname)  
#     else:  
#         if os.path.isfile(fullunzipdirname):  
#             print "File %s is exist, are you sure to delet it first ? [Y/N]" % fullunzipdirname  
#             while 1:  
#                 inputStr = raw_input()  
#                 if inputStr == "N" or inputStr == "n":  
#                     return  
#                 else:  
#                     if inputStr == "Y" or inputStr == "y":  
#                         os.remove(fullunzipdirname)  
#                         print "Continue to unzip files ..."  
#                         break  
              
#     #Start extract files ...  
#     srcZip = zipfile.ZipFile(fullzipfilename, "r")  
#     for eachfile in srcZip.namelist():
#         if eachfile.endswith('/'):
#             # is a directory
#             print 'Unzip directory %s ...' % eachfilename
#             os.makedirs(os.path.normpath(os.path.join(fullunzipdirname, eachfile)))
#             continue  
#         print "Unzip file %s ..." % eachfile  
#         eachfilename = os.path.normpath(os.path.join(fullunzipdirname, eachfile))  
#         eachdirname = os.path.dirname(eachfilename)  
#         if not os.path.exists(eachdirname):  
#             os.makedirs(eachdirname)  
#         fd=open(eachfilename, "wb")  
#         fd.write(srcZip.read(eachfile))  
#         fd.close()  
#     srcZip.close()  
#     print "Unzip file succeed!"