# vkusvil
#### Video Demo:  <URL HERE>
#### Description:
My project is meal constructor that makes mono (5 ingridients) and complicated (over 10 ingridient) products sold at ready to eat meals in a Moscow's groceries store. Ingridients will be local. I felt inspired to implement this idea in my project after eating chicken patties with mozarella and red bull pepper center and kinoa, carrot, pepper, bulgur as side dish. I think this groceries store is using software to come up with such complex ideas for meals. Some ingridients cannot match.
  I want to create a webapplication that
  I can add and edit certain ingridients to the db. Ingridients are marked and each meal has to have 20% fiber source, 30% fats, 30% protein, 10% superfoods, 10% carbs but not proccessed. Ingridients have provider mark like what company brings in the ingridient and what's its rate.
  make a meal button constructs a meal from the actual ingridients
  you can see a gallery of ingridients
  a user can check out their allergies
so db for an ingridient looks like this:

meal_id, created, content
user_id, name, hash
meal_id, content, user_id of the user who received this meal
ingridient_id, title, category

  User inputs ingridients and the programm outputs a meal constaining ingridient from each category
  programm compares the initial string (from recipe book) to the ingridients provided by the user and outputs the "recipe" with biggest amount of similarities
  how to implement in python the amount of similarities
  recipe "corn and lamb": corn, lamb, onion, butter, salt
  recipe "good": corn, ginger, cucumber, beef, tomato
  recipe "i can": potato, butter, bacon, rasperry
  user provided: lamb, butter, corn, cucumber
  the function:
  recipe_dict is a dict of dicts and new_dict is a dict called from db (select * from recipes) ['title'], ['ingridients']
  so  recipe_dict[new_dict] = count
  for k in recipe_dict:
    new_dict = {}
    for i in user_provided:
      if i in k['ingridients']:
        new_dict[k['title']] =+
  print(sorted(new_dict.items())[-1])
  
  
  dict of dict? title ingridients count
  first i'll write an app that finds keywords in posts then i can add registration
  my project currently is a web app that searches posts by keywords provided by the user
  
  I was following this tutorial (https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3) for creating a web app that can create and edit posts without authorisation. I decided that my web app will display videos subtitles (auto-generated or manual) as posts and search for relatable "posts" by inserted keywords. that's why I added a few more columns to the posts table such as author and title of the video. So posts are added by the link user adds. this app can be useful for finding explanation for a term but in a video format. 
  Youtube api returns subtitles as a dcitionary ([text], [start], [duration]) so I'm adding additional column to my posts table called start for my app to display the needed line but no i won't add another column I will just add this dictionary into my content column so that my posts["content"] is a dict in dict becuase it's important tp save where the term has been used
  i also decided to leave the design as it is because i don't mind chaos meaning I left "created" to be displaying when redirecting to "/<{{ post['id'] }}>"
