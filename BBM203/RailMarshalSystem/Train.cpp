#include "Train.h"
#include <iostream>

Train::Train() : name(""), destination(Destination::OTHERS), totalWeight(0), nextLocomotive(nullptr) {}
Train::Train(const std::string &_name, Destination _dest) : name(_name), destination(_dest), totalWeight(0), nextLocomotive(nullptr) {}
Train::~Train() { clear(); }


void Train::appendWagonList(WagonList &wl)
{
    wagons.appendList(std::move(wl));
    totalWeight = wagons.getTotalWeight();
}

void Train::addWagonToRear(Wagon *w)
{
    wagons.addWagonToRear(w);
    totalWeight = wagons.getTotalWeight();
}

// Removes all wagons and resets the train's data members used by destructor and reset operations.
void Train::clear()
{ 
    wagons.clear();
    totalWeight = 0;
    nextLocomotive = nullptr;
}

void Train::print() const
{
    std::cout << "Train " << name << " (" << totalWeight << " tons): ";
    std::cout << wagons << std::endl;
}

// Checks if any connection between wagons is overloaded. If the trailing wagons exceed 
// the next wagon's max load, the train is spit at that point. returns a new Train object
// if split occurs
Train *Train::verifyCouplersAndSplit(int splitCounter)
{

    if (wagons.isEmpty())
        return nullptr;

    Wagon *cur = wagons.getRear();  // Starts from last wagon
    int trailingWeight = 0;         // Total weight pulled by each coupler

    while (cur) {

        trailingWeight += cur -> getWeight();

        Wagon *pivot = cur -> getPrev();  // Wagon in front of the current one

        if (pivot) {

            // Check if the weight exceeds the pivot wagon's coupler capacity
            if (trailingWeight > pivot -> getMaxCouplerLoad()) {

                int splitStartId = cur -> getID();
                std::cout << "Train " << name << " split due to coupler overload before Wagon " << splitStartId << std::endl;

                // Create a new list of wagons starting from the overloaded point
                WagonList splitList = wagons.splitAtById(splitStartId);
                std::cout << splitList << std::endl;

                // Generate a new name for the split train
                std::string newName = name + "_split_" + std::to_string(splitCounter);

                // Build a new Train for the detached wagons
                Train *newTrain = new Train(newName, destination);
                newTrain->appendWagonList(splitList);
                totalWeight = wagons.getTotalWeight();  // Update current train's total weight

                std::cout << "Train " << newTrain->getName() << " assembled after split with " << newTrain->getWagons() << " wagons." << std::endl;

                return newTrain;  // return the detached section
            }
        }

        cur = pivot;  // move one wagon closer to the front
    }

    // No overloads found, no split required
    return nullptr;
}