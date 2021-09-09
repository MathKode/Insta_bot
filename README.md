# Insta_bot
Ceci est une mini API qui utilise selenium pour intéragir avec instagram et ainsi, pouvoir coder votre bot insta !

Pour le faire fonctionner tapper ce qui suit dans votre code :
````
import insta_bot
mon_bot = insta_bot.Bot("username","password","/chromedriver")
`````
Une fois fait, vous pouvez allez sur un profil avec un 
````
mon_bot.go_to("profil_name")
`````
Les fonctions que vous pouvez éxecuter son les suivantes :

- **go_to(profil_name)**

Cette fonction permet de ce rendre sur la page d'un utilisateur
- **find_and_go(text_to_search,line_number)**

Cette fonction permet d'écrire un texte dans la bar de recherche et de se rendre au profil qui apparait à la ligne *line_number*
Par exemple, si vous faite un ***find_and_go("youtube",4)***, ce ira sur le profil : youtubemusic (ligne numéro 4 quand on cherche youtube)
<img src="/image/1.png" width="280" />
- **find_and_get(text_to_search)**

Cette fonction récupère l'ensemble des possibilité de compte quand on tape *text_to_searc*. Par exemple, si on reprend lexemple prècèdent et qu'on cherche youtube, le code nous retournera 

`````
import insta_bot
n = insta_bot.Bot("name","mp","/chromedriver")
print(n.find_and_get("youtube"))
`````

*['youtube\nYouTube', 'gossipyoutubefr\nGOSSIP YOUTUBE ⭐️', 'youtubeupd8s\nYouTube Updates', 'fearless_ig\nFe4RLess YouTube', 'socialmediayoutubers\nMulti Fanpage', 'youtube.tj\n𝐘𝐎𝐔𝐓𝐔𝐁𝐄.𝐓𝐉 (𝟏𝟎𝟎𝐤) 🕊🤍', ...]*


- **get_follower_number(profil_name)**

Cette fonction renvoit le nombre d'abonné d'une personne (elle fait même la conversion entre les 45m -> 45 000 000 et 6k -> 6 000)

- **get_followed_number(profil_name)**

Cette fonction renvoit le nombre d'abonnement d'une personne

- **get_profil_info(profil_name)**

Cette fonction renvoit une liste de trois nombre [publication, abonnés, abonnements] (mais ne fait pas de convertion)

- **get_profil_name()**

Retourne le nom du compte de la page sur laquelle vous vous trouvez (Cela retourne 0 si vous n'êtes pas sur un profil)

- **get_driver()**

Retourne le driver selenium (pour continuer à coder avec...)

- **url() **

Retourne l'url de la page

- **open_message() **

Ouvre la messagerie

- **get_conversation_list() **

Ouvre la messagerie si elle est fermé et récupère les pseudos de toutes les personnes avec qui vous avez une conversation

- **send_to(profil, message)**

Envoie le message *message* à *profil*.

- **last_message(profil)**

Récupère les dernier message échangé avec *profil*

- **close()**

Ferme le navigateur

# Info

Ce code fonctionne sans time.sleep : vous n'avez pas à en mettre dans votre code...

**NON**
````
follower_list = b.get_follower_list("youtube")
time.sleep(5)
for i in follower_list:
    b.send_to(i,"Bonjour :-)")
`````

**OUI**
````
follower_list = b.get_follower_list("youtube")
for i in follower_list:
    b.send_to(i,"Bonjour :-)")
`````
