```plantuml

class Bot
{
    Donator [] m_donators
    Receivr [] m_receivers;
    dict m_handlers;
    dict s_flow_graph;

    void add_handler();
    void action(request);
}

class donator
{
telegram_id m_id;
float m_donator_level;
location m_location;
Foods[] m_open_foods;
Food m_food_being_built;
int m_donationCounter;

void manageFoods();
Foods donate();
}

class donationProcess
{

    void donate();
'   donator or receiver
    void select_location();
    ' foodType[] select_food_type();
    int select_expiration_day();
  int selectSizeOfSeriving();
'   void addDonationInfo();
'   photo uploadPhoto();
'   string addDiscription();
}

class ReceivingProcess
{
    void select_location();
    void show_relevant_foods();
}

class Database
{
    void createDonator();
    void createReciver();
    void updateDantor(donator i);
    void updateReciver(reciver i);

    void addFoods(Foods i);
    void markOfferAsDonated(Foods)a
}

package utils
{
}
class UIbuttons
{
 string headline;
<string,value>[] choices;
inlineKeyboardMarkup getButtons();
}

class reciver
{
 telegram_id m_id;
 food_type [] m_foods_type;
location m_location;

' void selectDesiredFood();<same as in donationProcess>
' void updateCurrentPosition();
Foods[] getRelevantFoods();
float get_relative_distance(Foods food);

 Location current_location;
'  foodType[] desiredFood;
'  void updateIntrestInAutomaticFoodss()
}

' class controller
' {
'  recivers[] m_recivers;

'  void updateIntrestedReciversAboutOffer(Foods i_Foods);
' void updateRecivers()
' void removeExpiredFoodss();
' }

enum foodType
{
kosher
halal
vegetarian
Vegan
animal_food
other
}

class Location
{
    longitude x;
    latitude y;

    string get_address();
}

class Photo
{
    int m_id;
    string m_path;
    m_img;
}

class Food
{
int m_food_id;
food_type[] m_foodTypes;
Donator m_donator;
Location m_location
Photo [] m_photos;

int m_number_of_servings;
int m_expiration_date;
string m_description;

string toString();
}

' class FoodsMap
' {
 
'  buildFoodsMap(Foodss[] relevantFoodss);
'  string getFoodssMapUrl();
' }



class multiChoice
{



 multiChoice(string[] choices);
 InlineKeyboardMarkup getButtons();
 InlineKeyboardMarkup selectChoice(int choiceNumber);
 stirng[] getSelectedChoices();
 string headline;
 string[] choices;
 bool[] selectedChoices;

}





```