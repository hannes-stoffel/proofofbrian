import os
from datetime import datetime, timedelta, date
from beem import Hive
from beem.account import Account
from beem.amount import Amount
from beem.blockchain import Blockchain
from beem.comment import Comment
from beem.exceptions import ContentDoesNotExistsException
from beem.instance import set_shared_blockchain_instance
import random


FILENAME_BLOCKNUM = 'current_block.txt'
FILENAME_POSTING = 'posting.txt'
FILENAME_NOTIFIED = 'notified.txt'


def get_last_block_number():
    if not os.path.exists(FILENAME_BLOCKNUM):
        return None

    with open(FILENAME_BLOCKNUM, 'r') as infile:
        block_num = infile.read()
        block_num = int(block_num)
        return block_num

def set_last_block_number(block_num):
    with open(FILENAME_BLOCKNUM, 'w') as outfile:
        outfile.write('%d' % block_num)

notified = []
if  os.path.exists(FILENAME_NOTIFIED):
    with open(FILENAME_NOTIFIED,'r') as f:
        for l in f:
            notified.append(l.strip())
        
posting = ''
with open(FILENAME_POSTING,'r') as f:
    for l in f:
        posting = l.strip()
        
postacc = 'proofofbrian'

#node = 'http://rpc.ausbit.dev'
#node = 'https://api.deathwing.me'
node='https://api.openhive.network' #'https://api.hive.blog'
hive = Hive(node=[node], keys={'posting':posting})
#hive = Hive(node=[node])
set_shared_blockchain_instance(hive)
chain = Blockchain()

gifs=[
    {'Pic':'https://upload.wikimedia.org/wikipedia/commons/0/0a/Brian_May_2015.jpg', 
     'Source':'https://commons.wikimedia.org/wiki/File:Brian_May_2015.jpg'}, 
    {'Pic':'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Professor_Brian_Cox_OBE_FRS.jpg/320px-Professor_Brian_Cox_OBE_FRS.jpg', 
     'Source':'https://commons.wikimedia.org/wiki/File:Professor_Brian_Cox_OBE_FRS.jpg'}, 
    {'Pic':'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Brian_Cant_2008.jpg/450px-Brian_Cant_2008.jpg',
     'Source':'https://commons.wikimedia.org/wiki/File:Brian_Cant_2008.jpg'},
    {'Pic':'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Brian_Cox_%282016%29_-_01.jpg/361px-Brian_Cox_%282016%29_-_01.jpg', 
     'Source':'https://commons.wikimedia.org/wiki/File:Brian_Cox_(2016)_-_01.jpg'},
    {'Pic':'https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Brian_Johnson.jpg/481px-Brian_Johnson.jpg', 
     'Source':'https://commons.wikimedia.org/wiki/File:Brian_Johnson.jpg'},
    {'Pic':'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Brian_Wilson_%287314673472%29_%28tall%29.jpg/450px-Brian_Wilson_%287314673472%29_%28tall%29.jpg', 
     'Source':'https://en.wikipedia.org/wiki/File:Brian_Wilson_(7314673472)_(tall).jpg'},
    {'Pic':'https://upload.wikimedia.org/wikipedia/commons/c/cc/Brian_Eno_-_TopPop_1974_12.png', 'Source':'https://commons.wikimedia.org/wiki/File:Brian_Eno_-_TopPop_1974_12.png'}
]

def addComment(comm):
    image = random.choice(gifs)
    text = f'''Here is your Proof of Brian. I think you meant #ProofOfBrain
![Brian]({image["Pic"]})
[Source]({image["Source"]})'''
    comm.reply(body=text,author=postacc)
    #return text




tracktags = set(['poofofbrain', 
                 'profeofbrain',
                 'proffofbrain',
                 'profofbrain', 
                 'profofbrian', 
                 'profoofbrain',
                 'proodofbrain',
                 'proofbrian',
                 'prooffbrain', 
                 'proofobbrain', 
                 'proofobrain',
                 'proofodbrain',
                 'proofofbain', 
                 'proofofbrai',
                 'proofofbran',
                 'proofofbrane', 
                 'proofofbrian', 
                 'proofofbrin', 
                 'proofofpbrain',
                 'proofofrain', 
                 'proofofrbrain',
                 'proofoofbrain', 
                 'proofoffbrain', 
                 'prooforbrain'
                 'proofotbrain',
                 'proofpfbrain',
                 'prooofbrian',
                 'prooofbrain',
                 'proooffbrain', 
                 'prooofofbrain', 
                 'proorofbrain',
                 'propfofbrain',
                 'proveofbrain',
                 'prrofofbrain',
                 'prufofbrain', 
                 'rofofbrain',
                 'roofofbrain',
                ])


while True:
    try:
        current_blocknum = get_last_block_number()
        if current_blocknum is not None:
            print(f'Resume work at block #{current_blocknum}')
        else:
            print('No blocknum given. Going with live feed.')
        for post in chain.stream(opNames="comment", start = current_blocknum, threading=True, thread_num=5):
            if (post['block_num'] != current_blocknum):
                current_blocknum = post['block_num']
                set_last_block_number(current_blocknum)
                print(f'Reading Block #{current_blocknum}')
            author = post['author']
            c = Comment(post)
            if c.is_main_post() and author not in notified and len(post['tags']) and tracktags.intersection(post['tags']):
                #ismain = Comment(post).is_main_post()
                print(f"Found one {author,post['title']} {post['timestamp']}")
                print(post['tags'])
                addComment(c)
                c.upvote(voter=postacc)
                notified.append(author)
                print(f'Total notified: {len(notified)}')
                with open(FILENAME_NOTIFIED, 'a') as f:
                    f.write(f'{author}\n')
    except Exception as error:
        print(repr(error))
        continue



