from google.cloud import aiplatform
import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair
import flet as ft

MODEL_PARAMETERS = {
        "candidate_count": 1,
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
        "4 cuisses de poulet"
        "1 kg de riz",
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
        "un rôti de porc",
        "un paquet de macaronis",
        "1 pack de 6 bouteilles d'eau d'Evian",
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
        "des tranches de jambon",
        "1 pack de 6 bouteilles d'eau d'Hépar",
        "3 baguettes"
     ],
]

def get_context():
    context = "Tu es mon assistant de courses."
    context += "Je fais les courses toutes les semaines, tu me donnes des indications sur ce que je dois acheter. "
    context += "Tu es capable de me dire quelles catégories de produits j'ai oublié par rapport aux semaines précédentes. Sois concis, sans rentrer dans les détails. "
    context += "Par exemple, tu oublies d'acheter du pain et du lait. "
    context += "Tu m'avertis aussi si j'achète des produits en double cette semaine. "
    for shopping in SHOPPINGS:
        items = ", ".join(shopping).strip()
        context += f"Une semaine précedente, j'avais acheté : {items}. "
    return context

def get_model():
    vertexai.init(project="yan-playground-395409", location="us-central1")
    return ChatModel.from_pretrained("chat-bison").start_chat(context=get_context())

def main(page: ft.Page):
    # see https://flet.dev/docs/tutorials/python-realtime-chat
    model = get_model()
    chat = ft.Column()
    def ask(e):
        user_message = new_message.value
        new_message.value = ""
        chat.controls.append(ft.Container(content=ft.Text(user_message), alignment=ft.alignment.center_right, bgcolor=ft.colors.BLUE_200, padding=10, margin=10, border_radius=5))
        bot_response = model.send_message(user_message, **MODEL_PARAMETERS)
        chat.controls.append(ft.Container(content=ft.Text(bot_response.text), alignment=ft.alignment.center_left, bgcolor=ft.colors.BLUE_400, padding=10, margin=10, border_radius=5))
        page.update()

    new_message = ft.TextField(on_submit=ask)
    page.add(chat, ft.Row(controls=[new_message]))
    page.update()


ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER
)