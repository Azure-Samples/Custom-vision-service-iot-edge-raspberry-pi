namespace DisplayIO
{
    using System;
    using System.IO;
    using System.Runtime.InteropServices;
    using System.Runtime.Loader;
    using System.Security.Cryptography.X509Certificates;
    using System.Text;
    using System.Threading;
    using System.Threading.Tasks;
    using Microsoft.Azure.Devices.Client;
    using Microsoft.Azure.Devices.Client.Transport.Mqtt;

    class Program
    {
        static int counter;

        static void Main(string[] args)
        {
            Init().Wait();

            // Wait until the app unloads or is cancelled
            var cts = new CancellationTokenSource();
            AssemblyLoadContext.Default.Unloading += (ctx) => cts.Cancel();
            Console.CancelKeyPress += (sender, cpe) => cts.Cancel();
            WhenCancelled(cts.Token).Wait();
        }

        /// <summary>
        /// Handles cleanup operations when app is cancelled or unloads
        /// </summary>
        public static Task WhenCancelled(CancellationToken cancellationToken)
        {
            var tcs = new TaskCompletionSource<bool>();
            cancellationToken.Register(s => ((TaskCompletionSource<bool>)s).SetResult(true), tcs);
            return tcs.Task;
        }

        /// <summary>
        /// Initializes the ModuleClient and sets up the callback to receive
        /// messages containing temperature information
        /// </summary>
        static async Task Init()
        {
            MqttTransportSettings mqttSetting = new MqttTransportSettings(TransportType.Mqtt_Tcp_Only);
            ITransportSettings[] settings = { mqttSetting };

            // Open a connection to the Edge runtime
            ModuleClient ioTHubModuleClient = await ModuleClient.CreateFromEnvironmentAsync(settings);
            await ioTHubModuleClient.OpenAsync();
            Console.WriteLine("IoT Hub module client initialized.");

            // Register callback to be called when a message is received by the module
            await ioTHubModuleClient.SetInputMessageHandlerAsync("input1", ProcessReceivedMessage, ioTHubModuleClient);
        }

        /// <summary>
        /// This method is called whenever the module is sent a message from the EdgeHub. 
        /// It prints all the incoming messages.
        /// </summary>
        static async Task<MessageResponse> ProcessReceivedMessage(Message receivedMessage, object userContext)
        {
            int counterValue = Interlocked.Increment(ref counter);

            var moduleClient = userContext as ModuleClient;
            if (moduleClient == null)
            {
                throw new InvalidOperationException("UserContext doesn't contain " + "expected values");
            }

            byte[] messageBytes = receivedMessage.GetBytes();
            string messageString = Encoding.UTF8.GetString(messageBytes);


            Console.WriteLine($"Received message: {counterValue}, Body: [{messageString}]");
//            Console.WriteLine($"{DateTime.Now}> {formattedMessage}");

            if (!string.IsNullOrEmpty(messageString))
            {
                using (var rxMessage = new Message(messageBytes))
                {
//                    string highestProbabilityTag = null;
//                    double highestProbably = 0;
                    foreach (var prop in receivedMessage.Properties)
                    {
                        if (prop.Key == "predictions")
                        {
                            Console.WriteLine("predictions:");
                            var predictionProp = prop.Value;
                            foreach (var pProp in predictionProp)
                            {
//                                if (Equals(pProp.Key.ToString, "probability")
//                                {
//                                    Console.WriteLine("prob:" + pProp.Value.ToString());
//                                    Console.WriteLine("tag:" + prop.Value);
//                                }
                            }
                        }
                        rxMessage.Properties.Add(prop.Key, prop.Value);
                    }
                    await moduleClient.SendEventAsync("output1", rxMessage);
                
                    Console.WriteLine("Received message sent");
                }
            }
            return MessageResponse.Completed;
        }
    }
}
