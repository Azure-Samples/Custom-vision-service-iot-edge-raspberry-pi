using System.Device.Gpio;
using System.Device.Gpio.Drivers;
using Microsoft.Azure.Devices.Client;
using Microsoft.Azure.Devices.Client.Transport.Mqtt;
using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.InteropServices;
using System.Runtime.Loader;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;

namespace DisplayIO
{
    internal class Program
    {
        static int counter;
        static int GPIO_A;
        static int GPIO_B;
        static double threshold = 0.99;
        static GpioController gpioController;

        static void Main(string[] args)
        {
            GPIO_A = Convert.ToInt32(Environment.GetEnvironmentVariable("GPIO_A"));
            GPIO_B = Convert.ToInt32(Environment.GetEnvironmentVariable("GPIO_B"));
            threshold = Convert.ToDouble(Environment.GetEnvironmentVariable("Threshold"));
            Console.WriteLine($"Threshold: {threshold}");
            if (Architecture.Arm64 == RuntimeInformation.ProcessArchitecture)
            {
                gpioController = new GpioController(PinNumberingScheme.Logical, new LibGpiodDriver(0));

                // both off
                gpioController.OpenPin(GPIO_A, PinMode.Output);
                gpioController.Write(GPIO_A, PinValue.Low);
                gpioController.OpenPin(GPIO_B, PinMode.Output);
                gpioController.Write(GPIO_B, PinValue.Low);
            }

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
            await ioTHubModuleClient.SetInputMessageHandlerAsync("input1", receiveMessage, ioTHubModuleClient);
        }


        public class RxMessage
        {
            public class Predictions
            {
                public string boundingBox { get; set; }
                public double probability { get; set; }
                public string tagId { get; set; }
                public string tagName { get; set; }
            }

            public DateTimeOffset created { get; set; }
            public string id { get; set; }
            public string itteration { get; set; }
            public IList<Predictions> predictions { get; set; }
            public string project { get; set; }

        }


        /// <summary>
        /// This method is called whenever the module is sent a message from the EdgeHub. 
        /// It prints all the incoming messages.
        /// </summary>
        static async Task<MessageResponse> receiveMessage(Message message, object userContext)
        {
            int counterValue = Interlocked.Increment(ref counter);

            var moduleClient = userContext as ModuleClient;
            if (moduleClient == null)
            {
                throw new InvalidOperationException("UserContext doesn't contain " + "expected values");
            }

            byte[] messageBytes = message.GetBytes();
            string messageString = Encoding.UTF8.GetString(messageBytes);
            Console.WriteLine($"Received message: {counterValue}, Body: [{messageString}]");
            
            if (!string.IsNullOrEmpty(messageString))
            {
                double highestProbability = 0;
                string highestProbabilityTag = string.Empty;

                RxMessage rxMessage = JsonSerializer.Deserialize<RxMessage>(messageString);

                foreach (var predicts in rxMessage.predictions)
                {
                    if (predicts.probability > highestProbability && predicts.probability > threshold)
                    {
                        highestProbability = predicts.probability;
                        highestProbabilityTag = predicts.tagName;
                        string highestProbabilityS = String.Format("{0:0.00}", highestProbability);
                        Console.WriteLine("tagID: " + highestProbabilityTag + " Probability: " + highestProbabilityS);
                        if (Architecture.Arm64 == RuntimeInformation.ProcessArchitecture)
                        {
                            if (0 == string.Compare(highestProbabilityTag, "Apple"))
                            {
                                gpioController.Write(GPIO_A, PinValue.High);
                                gpioController.Write(GPIO_B, PinValue.Low);
                            }
                            if (0 == string.Compare(highestProbabilityTag, "Banana"))
                            {
                                gpioController.Write(GPIO_A, PinValue.Low);
                                gpioController.Write(GPIO_B, PinValue.High);
                            }
                        }
                    }
                }

                using (var pipeMessage = new Message(messageBytes))
                {
                    foreach (var prop in message.Properties)
                    {
                        pipeMessage.Properties.Add(prop.Key, prop.Value);
                    }
                    await moduleClient.SendEventAsync("output1", pipeMessage);

                    Console.WriteLine("Received message sent");
                }
            }
            return MessageResponse.Completed;
        }
    }
}
