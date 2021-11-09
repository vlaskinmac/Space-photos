# Space photos - Devman

**Script sends a photo of the planet earth to the telegram channel.**


This script is written as part of the task of the courses [Devman](https://dvmn.org).

- When the code is run, photos are sent to the specified telegram channel. 

- By default with a period of once a day. Or in a user-defined period. 

- The photos were obtained from the [NASA](https://www.nasa.gov) website.

- Photos in real color.

<img src="https://user-images.githubusercontent.com/78322994/140647471-a178cbd6-4d2a-4387-8db4-7c74b344a680.png" alt="drawing" width="200"/>  

- The script also downloads photos of the last [NASA](https://www.nasa.gov) launch:

<img src="https://user-images.githubusercontent.com/78322994/140932027-ef5be459-74fa-470d-bb28-25807e2e5943.jpg" alt="drawing" width="200"/>

- And uploads a photo of the day of space from [NASA](https://www.nasa.gov):

<img src="https://user-images.githubusercontent.com/78322994/140932208-35b01f9f-c6d5-4428-97b7-fda3c31a4d36.jpg" alt="drawing" width="200"/> 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Python Version

Python 3.6 and later.

### Installing

To install the software, you need to install the dependency packages from the file: **requirements.txt**.

Perform the command:

```

pip3 install -r requirements.txt

```


## Getting API key

**API key NASA**

- To get the API key. You need to log in to the API service NASA link: [`API-NASA`](https://api.nasa.gov/).
- On the main page, fill out the form and generate API key.

**API key Telegram bot**

- Go to Telegram. 
- Call the system bot by typing in the search: [@BotFather](https://telegram.me/BotFather) 
- Enter the command:
```
/token
```


### Connecting the API key

You need to create a `.env` file and write all sensitive data into it, like this:

```python
API_KEY_NASA="272a05d39ec46fdac5be4ac7be45f3f"
API_KEY_BOT="2127492642:AAFC4-Ey3WTtFNCcSzbDN7Z7y1ePaw8IbTU"
CHAT_ID = -1001647060957
```

## Launch code
#### Arguments
- Set the update period in hours use arguments: **-hh** or **--hours**
- Set the update period in seconds use arguments: **-s** or **--seconds**
- Uploads a photo of space day use arguments: '-a or --apoid' and command: **`APOID`**
- Uploads photos of the last [NASA](https://www.nasa.gov) launch use arguments: '-l or --last' and command: **`LAST`**
- To call help, use the required arguments **-h** or **--help**

**Examples of commands:**

```python
$ python photos_space.py --seconds 30
```

```python
$ python photos_space.py --hours 4
```

- Running code without arguments the default period is once every 24 hours:
```python
$ python photos_space.py 
```

- Uploads a photo of space day:
```python
$ python photos_space.py -a APOID
```

- Uploads photos of the last [NASA](https://www.nasa.gov) launch:
```python
$ python photos_space.py -l LAST
```

## Authors

**vlaskinmac**  - [GitHub-vlaskinmac](https://github.com/vlaskinmac/)


