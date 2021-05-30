import pika, sys, os,json

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='upload')

    def callback(ch, method, properties, body):

        req=json.loads(body)
        print("***")
        print(req)
        # print(req)
        # print(" [x] Received %r" % body)

    channel.basic_consume(queue='upload', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)