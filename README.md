# Space photos - Devman

**Script sends a photo of the planet earth to the telegram channel.**


This script is written as part of the task of the courses [Devman](https://dvmn.org).

- When the code is run, photos are sent to the specified telegram channel. 

- By default with a period of once a day. Or in a user-defined period. 

- The photos were obtained from the [NASA](https://www.nasa.gov) website.

- Photos in real color.


<img src="https://user-images.githubusercontent.com/78322994/140647471-a178cbd6-4d2a-4387-8db4-7c74b344a680.png" alt="drawing" width="200"/> <img src="https://user-images.githubusercontent.com/78322994/140647474-46b29d3f-5227-4c11-b3c1-67a0ba0678eb.png" alt="drawing" width="200"/> <img src="https://user-images.githubusercontent.com/78322994/140647475-18735c1d-5dbb-44e2-a9a0-35041bb8e7a1.png" alt="drawing" width="200"/> <img src="https://user-images.githubusercontent.com/78322994/140647478-6d43996f-9208-4b7f-a737-93e9a2d64605.png" alt="drawing" width="200"/> <img src="https://user-images.githubusercontent.com/78322994/140647479-1d896c98-6e9a-4a4b-b528-86ce3bf7ab36.png" alt="drawing" width="200"/> <img src="https://user-images.githubusercontent.com/78322994/140647481-1d167daf-078d-4c9c-b5a7-11c59b5509ca.png" alt="drawing" width="200"/>


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

## Variables

- Сhat id must be registered in the **CHAT_ID** constant.

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
```

## Launch code
#### Arguments
- Set the update period in hours use arguments: **-hh** or **--hours**
- Set the update period in seconds use arguments: **-s** or **--seconds**
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

## Authors

**vlaskinmac**  - [GitHub-vlaskinmac](https://github.com/vlaskinmac/)


