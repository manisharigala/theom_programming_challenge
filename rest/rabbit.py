
import pika,os,time

def connectToRabbitMQ():
    channel = None
    count=0
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBIT_ADDRESS']))
            channel = connection.channel()
            break
        except:
            print("trying to connect to rabbit.....")
            if count>5:
                raise Exception("Cannot establish connection to Rabbit!")
                exit(0)
            time.sleep(5)
            count+=1
            continue
    return channel

def publishToQueue(queueName, data):
    channel = connectToRabbitMQ()
    
    channel.queue_declare(queue=queueName)
    
    channel.basic_publish(exchange='',
                      routing_key=queueName,
                      body=data)
    return 1