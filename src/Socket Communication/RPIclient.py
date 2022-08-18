import serial
import json
import time

data = []


def main():
    try:
        serMega = serial.Serial("/dev/ttyACM0", 115200)  # IMU Fast Data located here

        while True:
            data = serMega.readline().decode('utf-8').split()
            # print(data)

            # Splitting the array into separated battery id arrays
            size = 4
            battery_id1 = [0] * size
            battery_id2 = [0] * size
            battery_id3 = [0] * size
            battery_id4 = [0] * size

            for i in range(16):
                if 0 <= i <= 3:
                    battery_id1[i] = data[i]  # storing elements 0-3 of "array_Element" in "battery_id1"
                elif 4 <= i <= 7:
                    battery_id2[i - 4] = data[i]  # storing elements 4-7 of "array_Element" in "battery_id2"
                elif 8 <= i <= 11:
                    battery_id3[i - 8] = data[i]  # storing elements 8-11 of "array_Element" in "battery_id3"
                elif 12 <= i <= 15:
                    battery_id4[i - 12] = data[i]  # storing elements 12-15 of "array_Element" in "battery_id4"

            print("Battery 1: ", battery_id1)
            print("Battery 2: ", battery_id2)
            print("Battery 3: ", battery_id3)
            print("Battery 4: ", battery_id4)

            # Creating a dictionary to dump the array data into a file
            dictionary = {
                "Battery Data": [
                    {
                        "Cell 1 Voltage": battery_id1[0],
                        "Cell 2 Voltage": battery_id1[1],
                        "Cell 3 Voltage": battery_id1[2],
                        "Cell 4 Voltage": battery_id1[3]
                    },
                    {
                        "Cell 1 Voltage": battery_id2[0],
                        "Cell 2 Voltage": battery_id2[1],
                        "Cell 3 Voltage": battery_id2[2],
                        "Cell 4 Voltage": battery_id2[3]
                    },
                    {
                        "Cell 1 Voltage": battery_id3[0],
                        "Cell 2 Voltage": battery_id3[1],
                        "Cell 3 Voltage": battery_id3[2],
                        "Cell 4 Voltage": battery_id3[3]
                    },
                    {
                        "Cell 1 Voltage": battery_id4[0],
                        "Cell 2 Voltage": battery_id4[1],
                        "Cell 3 Voltage": battery_id4[2],
                        "Cell 4 Voltage": battery_id4[3]
                    }
                ]
            }

            # Serializing json
            json_object = json.dumps(dictionary, indent=4)

            # Writing to file BatteryDataDump.json
            with open("GetBMSDataDump.json", "w") as outfile:
                outfile.write(json_object)

            time.sleep(3)

    except:
        print("An ERROR has occured!!!")
        print("Restart in Progress... Data resyncing")
        main()


if __name__ == "__main__":
    main()
