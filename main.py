from google.cloud import aiplatform
import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair
import flet as ft

MODEL_PARAMETERS = {
        "candidate_count": 1,
        "max_output_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }
SHOPPINGS = [
    [
        "6 bouteilles de lait",
        "4 yaourts à la vanille",
        "8 yaourts de chèvre",
        "1 camembert",
        "1 kilogramme de tomates",
        "2 concombres",
        "1 laitue",
        "5 bananes",
        "1 kilogramme de pommes",
        "1 pack de 6 bouteilles d'eau d'Evian",
        "une bouteille de vin de bordeaux"
     ],
[
        "6 bouteilles de lait",
        "4 yaourts à la vanille",
        "4 yaourts de chèvre",
        "1 reblochon",
        "1 kilogramme de tomates",
        "1 concombre",
        "1 chou-fleur",
        "5 bananes",
        "1 kilogramme de prunes",
        "1 pack de 6 bouteilles d'Evian",
        "une bouteille de côtes-du-rhône"
     ],
[
        "16 yaourts nature",
        "1 camembert",
        "du comté",
        "1,5 kilogramme de pommes de terre",
        "1 botte de radis",
        "6 kiwis",
        "1 kilogramme de pommes",
        "1 pack de 6 bouteilles d'Hépar",
        "3 baguettes"
     ],
]

def get_context():
    context = "Tu es mon assistant de courses."
    context += "Je fais les courses toutes les semaines, tu me donnes des indications sur ce que je dois acheter. "
    context += "Tu es capable de me dire quelles catégories de produits j'ai oublié par rapport aux semaines précédentes. Sois concis, sans rentrer dans les détails. "
    context += "Par exemple, tu oublies d'acheter du pain et du lait. "
    context += "Tu m'avertis aussi si j'achète des produits en double cette semaine. "
    context += "Par exemple : tu achètes beaucoup de laitages, tu ne trouves pas ? "
    for shopping in SHOPPINGS:
        items = ", ".join(shopping).strip()
        context += f"Une semaine précedente, j'avais acheté : {items}. "
    return context

def get_examples():
    return [
        InputOutputTextPair(
            input_text="Est-ce que j'ai oublié quelque chose cette semaine ?",
            output_text="Non, tu n'as rien oublié cette semaine."
        ),
        InputOutputTextPair(
            input_text="Est-ce que j'ai oublié quelque chose cette semaine ?",
            output_text="Oui, tu as oublié certains produits."
        )
    ]

def get_model():
    vertexai.init(project="yan-playground-395409", location="us-central1")
    return ChatModel.from_pretrained("chat-bison").start_chat(context=get_context(),examples=get_examples())

def main(page: ft.Page):
    # see https://flet.dev/docs/tutorials/python-realtime-chat
    model = get_model()
    chat = ft.ListView()
    def ask(e):
        user_message = new_message.value
        new_message.value = ""
        chat.controls.append(ft.Text(user_message, text_align=ft.TextAlign.RIGHT, bgcolor=ft.colors.BLUE))
        bot_response = model.send_message(user_message, **MODEL_PARAMETERS)
        chat.controls.append(ft.Text(bot_response.text, text_align=ft.TextAlign.LEFT, bgcolor=ft.colors.CYAN))
        page.update()

    new_message = ft.TextField(on_submit=ask)
    page.add(chat, new_message)
    page.update()




ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER
)