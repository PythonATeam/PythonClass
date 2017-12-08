import sys, string
if __name__ == "__main__":
	input_file= input("Input File:")
	with open(input_file,"r") as f:
		content= f.readlines()

developers={}
publishers={}
pub=[]
dev=[]
game=[]
av=[]
# id will be used for id primary key in sql insert statements
id=1
console_id=0   # used for gaming console id in "available" SQL table
established= "1999"
location="Atlanta"

#xbox1=1, xbox360=2, ps3=3, ps4=4, wii u= 5
for a in content:
    a=a.replace("[","")
    a=a.replace("]","")
    a=a.replace(" "" ", "")
    a= a.replace(" ' ", "")
    a= a.split("_")
    title=a[0]
    summary=a[1]
    if a[2]!= 'None':
        online_rating= float(a[2])
    if a[2] == 'None':
        online_rating= float(-999)
    developed_by=a[3]
    published_by=a[4]
    genre=a[5]
    price=float(a[6])
    #insert only unique publishers and developers into respective sets, and later on, tables
    if (published_by in publishers)==False:
        publishers[published_by]= id
    if(developed_by in developers)==False:
        developers[developed_by]= id


    if "\'Xbox One\'" in a[8]:
            console_id=1
    if "\'Xbox 360\'" in a[8]:
            console_id=2
    if "\'PlayStation 3\'" in a[8]:
            console_id=3
    if "\'PlayStation 4\'" in a[8]:
            console_id=4
    if "\'Nintendo Wii U\'" in a[8]:
            console_id=5
    image=a[9]
    #insert into game SQL table
    game.append("insert into game (id, title, summary, online_rating, developer_id, publisher_id,"
                " genre, price,image) values ({}, \"{}\", \"{}\", {}, {}, {}, \"{}\", {},\"{}\");\n".format(id, title,summary,online_rating,developers[developed_by],publishers[published_by],genre,price,image))
    #insert into available SQL table
    av.append("insert into available (id, game_id , console_id) values({},{},{});\n".format(id, id , console_id))
    id+=1

w = open('insert2.sql','w')
w.write("delete from available;\n")
w.write("delete from game;\n")
w.write("delete from publisher;\n")
w.write("delete from developer;\n")
#insertion statement into SQL publisher table
for a in publishers:
    w.write("insert into publisher (id, name) values ({},\"{}\");\n".format(publishers[a], a))
#insertion statement into SQL developer table
for a in developers:
    w.write("insert into developer (id, name) values ({},\"{}\");\n".format(developers[a], a))

for a in game:
    w.write(a)
for a in av:
    w.write(a)
w.close()