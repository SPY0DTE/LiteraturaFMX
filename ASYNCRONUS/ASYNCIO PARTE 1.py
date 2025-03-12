import asyncio #Importas la libreria asyncrona
import websockets#Importas los websockets
async def handler(websocket):#Esto es una manera de definir una corrutina llamada handler que será asyncrona
    while True:#Dentro de la corrutina vamos a recivir algo de Websocket y vamos a imprimirlo
        message = await websocket.recv()
        #We say a object is awaitable if it can be used in an await expresison.
        #Await can be:
        # Awaitables objects can be: Courutines, Tasks and futures
        # Web Socker.Recv() A function to receive the next message, when conection
        # Is closed recv() raises ConnectionClosedOk during a normal connection closure
        # Y manda ConnectionClosedError
        print(message)


async def main(): #La corrutina main   
    async with websockets.serve(handler, "", 8001): #Serve es una funcion que inicia un servidor listener de Websocket 
    #Esta funcion toma 3 argumentos: Una corrutina que maneja la coneccion
    # DEFINE LOS iNTERFACES DE RED DONDE EL SERVIDO PUEDE SER ALZANCADO.
    # El puerto donde el servidor va a estar escuchando
    # Async With  se usa porque Websocket.Serve is a context manager
    # Y asi se ejecuta un ayncronus context manager con "Async With" 
        await asyncio.Future()  # run forever
        # Future reoresent an eventual result of an asynchronous operation
        # Las Co-Rutinas pueder esperar en Objetos Futuros hasta que presenten un resultado o una excepción
if __name__ == "__main__": #Manera en la que El interprete de python leee el codigo y lo ejecuta
    asyncio.create_task(main()) #Run se utiliza para ejecutar una corutina y retornar un resultado.Pero  no usamos run porque Spyder runs its own event loop
    #Por eos creamos una nueva tarea para poder correr la corrutina no en ya creado thread de spiderman