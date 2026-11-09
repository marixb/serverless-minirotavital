import json, time

contador = 0

def lambda_handler(event, context):
    global contador
    contador += 1

    pedido = json.loads(event.get("body") or "{}")

    if "requisicaoId" not in pedido:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "erro": "requisicaoId obrigatório"
            })
        }

    if pedido.get("demorar"):
        time.sleep(5)

    guia = {
        "guia": "G-" + pedido["requisicaoId"],
        "hospital": pedido.get("hospital"),
        "bolsas": pedido.get("bolsas", []),
        "invocacaoNesteAmbiente": contador
    }

    return {
        "statusCode": 201,
        "body": json.dumps(guia)
    }