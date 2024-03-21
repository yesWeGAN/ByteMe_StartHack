# sandbox.py
import json
import src
import importlib
importlib.reload(src.vector_store.inference)
import numpy as np
import matplotlib.pyplot as plt 
from src.vector_store.inference import KNNSimpleInference

raw_data_path = "src/raw_stacks"
simpleInf = KNNSimpleInference(    inputpath=raw_data_path,
    outputpath="src/index_files",
    index_of_what='q'
)
all_related_dists = []  # related queries: the exact queries in the dataset (upper ceiling val)
all_questions = json.load(open("src/raw_stacks/all_questions.json"))
questions = [question.split(": ")[-1] for question in all_questions]
for q in questions:
    _,_,dists = simpleInf.inference(query=q, k=5, printprop=False)
    all_related_dists.append(dists)
all_related_dists

array_setup = []
for dist in all_related_dists:
    array_setup.append(np.array(dist))
arr = np.stack(array_setup)
arr.shape
fig, axes = plt.subplots()
for k in range(5):
    plt.hist(arr[:,k])
plt.savefig("disthist_related.png")
np.mean(arr, axis=0)    # array([0.26547362, 0.49442686, 0.55913755, 0.59787559, 0.62631579])
np.max(arr, axis=0)     # array([0.52122849, 0.77196632, 0.78859436, 0.79521986, 0.8066974 ])
np.min(arr, axis=0)     # array([0.13240061, 0.23253838, 0.23793852, 0.30774476, 0.34636679])

unrelated_queries = [
    "It's never been my responsibility to glaze the donuts.",
    "She hadn't had her cup of coffee, and that made things all the worse.",
    "Jenny made the announcement that her baby was an alien.",
    "You have every right to be angry, but that doesn't give you the right to be mean.",
    "The child’s favorite Christmas gift was the large box her father’s lawnmower came in.",
    "Rock music approaches at high velocity.",
    "You realize you're not alone as you sit in your bedroom massaging your calves after a long day of playing tug-of-war with Grandpa Joe in the hospital.",
    "For the 216th time, he said he would quit drinking soda after this last Coke.",
    "I'm worried by the fact that my daughter looks to the local carpet seller as a role model.",
    "The rain pelted the windshield as the darkness engulfed us.",
    "He poured rocks in the dungeon of his mind.",
    "There was coal in his stocking and he was thrilled.",
    "Bill ran from the giraffe toward the dolphin.",
    "This is a Japanese doll.",
    "I think I will buy the red car, or I will lease the blue one.",
    "The blinking lights of the antenna tower came into focus just as I heard a loud snap.",
    'Jason lived his life by the motto, "Anything worth doing is worth doing poorly."',
    "Andy loved to sleep on a bed of nails.",
    "Flash photography is best used in full sunlight.",
    "Don't piss in my garden and tell me you're trying to help my plants grow.",
    "Writing a list of random sentences is harder than I initially thought it would be.",
    "If you don't like toenails, you probably shouldn't look at your feet.",
    "The bird had a belief that it was really a groundhog.",
    "She was disgusted he couldn’t tell the difference between lemonade and limeade.",
    "The Guinea fowl flies through the air with all the grace of a turtle.",
    "He had unknowingly taken up sleepwalking as a nighttime hobby.",
    "He ended up burning his fingers poking someone else's fire.",
    "I am my aunt's sister's daughter.",
    "When he had to picnic on the beach, he purposely put sand in other people’s food.",
    "Of course, she loves her pink bunny slippers.",
    "The tumbleweed refused to tumble but was more than willing to prance.",
    "Standing on one's head at job interviews forms a lasting impression.",
    "I currently have 4 windows open up… and I don’t know why.",
    "Lucifer was surprised at the amount of life at Death Valley.",
    "Two more days and all his problems would be solved.",
    "The small white buoys marked the location of hundreds of crab pots.",
    "Imagine his surprise when he discovered that the safe was full of pudding.",
    "Car safety systems have come a long way, but he was out to prove they could be outsmarted.",
    "The knives were out and she was sharpening hers.",
    "The stranger officiates the meal.",
    "The worst thing about being at the top of the career ladder is that there's a long way to fall.",
    "The elephant didn't want to talk about the person in the room.",
    "She wore green lipstick like a fashion icon.",
    "They desperately needed another drummer since the current one only knew how to play bongos.",
    "The team members were hard to tell apart since they all wore their hair in a ponytail.",
    "It's much more difficult to play tennis with a bowling ball than it is to bowl with a tennis ball.",
    "I became paranoid that the school of jellyfish was spying on me.",
    "Greetings from the galaxy MACS0647-JD, or what we call home.",
    "The fish dreamed of escaping the fishbowl and into the toilet where he saw his friend go.",
    "When he encountered maize for the first time, he thought it incredibly corny."
]


all_unrelated_dists = []  # related queries: the exact queries in the dataset (upper ceiling val)

for q in unrelated_queries:
    _,_,dists = simpleInf.inference(query=q, k=5, printprop=False)
    all_unrelated_dists.append(dists)

array_setup2 = []
for dist in all_unrelated_dists:
    array_setup2.append(np.array(dist))
arr2 = np.stack(array_setup2)
arr2.shape
fig, axes = plt.subplots()
for k in range(5):
    plt.hist(arr2[:,k])
plt.savefig("disthist_unrelated.png")
np.mean(arr2, axis=0)    # array([0.8971205 , 0.90973786, 0.92059401, 0.92685773, 0.93348435])
np.max(arr2, axis=0)     # array([0.96119489, 0.9757248 , 0.98577503, 0.98596315, 0.99810633])
np.min(arr2, axis=0)     # array ([0.82980605, 0.84592813, 0.8636576 , 0.86863414, 0.87129115])
