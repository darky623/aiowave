# aiowave
Backend of simple social network for everyone

## Description of api functions

  + ### register
    POST localhost/api?func=register

    body:
      + nickname (str) (MAX: 16) (required)
      + firstname (str) (MAX: 16)
      + surname (str) (MAX: 16)
      + city (str) (MAX: 16)
      + website (url) (MAX: 120)
      + password (str) (MAX: 16) (required)
      + password_repeat (str) (MAX: 16) (required)
    
    Response: `{"token": token (str)}`
  
  + ### auth
    GET localhost/api?func=auth

    body:
      + nickname (str) (MAX: 16) (required)
      + password (str) (MAX: 16) (required)
   
    Response: `{"token": token (str)}`
   
  + ### new_post
    POST localhost/api?func=new_post

    body:
      + token (str) (required)
      + text (str) (MAX: 120) (required)
   
    Response: `{"id": post_id (int)}`

  + ### delete_post
    POST localhost/api?func=delete_post

    body:
      + token (str) (required)
      + post_id (int) (required)

  + ### all_posts
    GET localhost/api?func=all_posts

    body:
      + token (str) (required)

    Response: Array list:
      + `"post_id": post_id (int)`
      + `"author_id": author id (int)`
      + `"author_name": author nickname (str)`
      + `"text": text (str)`
      + `"date_created": date_created (str) (%d/%m/%Y %H:%M:%S)`
      + `"likes": number of likes (int)`
      + `"user_like":  user like status (boolean)`

   + ### like
     POST localhost/api?func=like

     body:
      + token (str) (required)
      + post_id (int) (required)

     Response: Array:
       + `"post_id": post_id (int)`
       + `"user_like": user like status (boolean)`

    
