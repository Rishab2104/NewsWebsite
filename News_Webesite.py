import streamlit as st


import requests


import mysql.connector as c;


con = c.connect(host='localhost', user='root', password='password', database='project')
cur = con.cursor()






def main():
   global category  
   st.title('News app')


   menu=['Home','Login','SignUp']
   choice=st.sidebar.selectbox('Menu',menu)


   if choice =='Home':
       st.subheader("Home")
       '''This news app was createad as a way to help create a personalized environment
       by the user; where the user can choose the category of news to be displayed'''


   elif choice=="Login":
       st.subheader("Login")


       username= st.sidebar.text_input("User name")
       password=st.sidebar.text_input("Password",type='password')
       usn=str(username)


       if st.sidebar.button("Login"):
           log="select password from login where username=(%s)"
           cur.execute(log,(usn,))
           pur=cur.fetchone()
           pwd=pur[0]
           if password==pwd:
               st.success("Logged in")  
               c='select category from login where username=(%s) '
               cur.execute(c,(usn,))
               cat=cur.fetchone()
               act=cat[0]
               tac=act.lower()




               
               url=f"https://newsapi.org/v2/top-headlines?country=us&category={tac}&apiKey=5f4b6487c3c7456b85263b1f8579bb93"
               r = requests.get(url)
               r = r.json()
               articles = r['articles']
               for article in articles:
                   st.header(article['title'])
                   st.write(article['publishedAt'])
                   if (article['author']):
                       st.write(article['author'])
                   st.write(article['source']['name'])
                   st.write(article['description'])
                   st.write(article['url'])
                   st.image(article['urlToImage'])




           else:
               st.warning("Incorrect Username/Password")


   elif choice=="SignUp":
       st.subheader("Create a New Account")
       new_user=st.text_input("Username")
       new_password=st.text_input("Password",type='password')
       category=['Business','Entertainment','General','Health','Science','Sports','Technology']
       new_genre=st.selectbox('News select Category',category)


       if st.button("SignUp"): 
           sig='select username from login '
           
           cur.execute(sig)
           un=cur.fetchall()
           if len(un)==0:
              ins="insert into login values(%s,%s,%s)"
              ud=(new_user,new_password,new_genre)
              cur.execute(ins,ud)
              con.commit()
              st.success("The account has been created")
              st.info("Go to login menu to login ")




           elif len(un)>0:
            for i in un:
                if new_user!=i[0]:
                  ins="insert into login values(%s,%s,%s)"
                  ud=(new_user,new_password,new_genre)
                  cur.execute(ins,ud)
                  con.commit()
                 
                  st.success("The account has been created")
                  st.info("Go to login menu to login ")
                else:
                  st.warning("Username already exists, please use a different username")
