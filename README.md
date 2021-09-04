# Insta_bot
Ceci est une mini API qui utilise selenium pour intéragir avec instagram et ainsi, pouvoir coder votre bot insta !

Pour le faire fonctionner tapper ce qui suit dans votre code :
````
import insta_bot
mon_bot = insta_bot.Bot("username","password")
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

Cette fonction récupère l'ensemble des possibilité de compte quand on tape *text_to_searc*. Par exemple, si on reprend lexemple prècèdent et qu'on cherche youtube, le code nous retournera [




