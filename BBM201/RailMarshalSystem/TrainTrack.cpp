#include "TrainTrack.h"
#include <iostream>

bool TrainTrack::autoDispatch = false;

TrainTrack::TrainTrack()
    : firstLocomotive(nullptr),
      lastLocomotive(nullptr),
      destination(Destination::OTHERS),
      totalWeight(0), trainCounter(0)
{
}

TrainTrack::TrainTrack(Destination _dest)
    : firstLocomotive(nullptr),
      lastLocomotive(nullptr),
      destination(_dest),
      totalWeight(0), trainCounter(0)
{
}

// Ensures that all trains currently on the track are properly
TrainTrack::~TrainTrack()
{
    while(firstLocomotive) {

        Train *departed = departTrain();
    

    }
}


std::string TrainTrack::generateTrainName()
{
    ++trainCounter;
    return "Train_" + destinationToString(destination) + "_" + std::to_string(trainCounter);
}

// Adds a train to the end of the track queue 
void TrainTrack::addTrain(Train *train)
{
    if (!train)
        return;

    // Attach train to the linked list of locomotives
    if (!firstLocomotive)
    {
        firstLocomotive = train;
        lastLocomotive = train;
    }
    else
    {
        // Append train to the end of the list
        lastLocomotive -> setNext(train);
        lastLocomotive = train;
    }

    totalWeight += train -> getTotalWeight();

    // Automatically dispatch trains if total weight exceeds limit. Dispatches from the front.
    while (autoDispatch && totalWeight > AUTO_DISPATCH_LIMIT && firstLocomotive) {

        Train *departed = departTrain();
        if (departed) {
            std::cout << "Auto-dispatch: departing " << departed -> getName() << " to make room.\n";
            departTrain();  
        }         
        
    }

}

// Removes the first train from the track and returns it. 
Train *TrainTrack::departTrain()
{
    if (!firstLocomotive)
        return nullptr;

    // Detach the first train
    Train *removed = firstLocomotive;
    firstLocomotive = firstLocomotive -> getNext();

    if (!firstLocomotive)
        lastLocomotive = nullptr;  // Track becomes empty

    totalWeight -= removed -> getTotalWeight();
    removed -> setNext(nullptr);

    std::cout << "Train " << removed -> getName() << " departed from Track " << destinationToString(destination) << "." << std::endl;

    delete removed;
    
    return nullptr;
}

// Returns true if there are no trains currently on the track.
bool TrainTrack::isEmpty() const
{
    if (firstLocomotive == nullptr)
        return true;
    return false;
}

// Searches for a train by its name within the track's linked list. returns a pointer 
// to the Train object if found, otherwise nullptr.
Train *TrainTrack::findTrain(const std::string &name) const
{
    Train *cur = firstLocomotive;
    while (cur)
    {
        if (cur -> getName() == name)
            return cur;
        cur = cur -> getNext();
    }

    return nullptr;
}

void TrainTrack::printTrack() const
{

    if (isEmpty())
        return;

    Train *current = firstLocomotive;

    std::cout << "[Track " << static_cast<int>(firstLocomotive->destination) << "] ";
    while (current)
    {
        std::cout << current->getName() << "(" << current->getTotalWeight() << "ton)-" << current->wagons << " -> ";
        current = current->getNext();
    }
    std::cout << std::endl;
    return;
}