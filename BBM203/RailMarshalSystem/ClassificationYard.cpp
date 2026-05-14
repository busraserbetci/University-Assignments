#include "ClassificationYard.h"
#include <iostream>

ClassificationYard::ClassificationYard() {}
ClassificationYard::~ClassificationYard() { clear(); }

WagonList &ClassificationYard::getBlockTrain(int destination, int cargoType)
{
    return blockTrains[destination][cargoType];
}

WagonList *ClassificationYard::getBlocksFor(Destination dest)
{
    return blockTrains[static_cast<int>(dest)];
}

void ClassificationYard::insertWagon(Wagon *w)
{
    if (!w)
        return;
    int dest = static_cast<int>(w->getDestination());
    int cargo = static_cast<int>(w->getCargoType());
    blockTrains[dest][cargo].insertSorted(w);
}

// Collects all wagons for a given destination and assembles them into a single train
// according to cargo type (weight, hazardous etc)
Train *ClassificationYard::assembleTrain(Destination dest, const std::string &trainName)
{
    WagonList *blocks = getBlocksFor(dest);

    // Check if there are any wagons for destination
    bool anyWagon = false;
    for (int j = 0; j < NUM_CARGOTYPES_INT; ++j)
    {
        if (!blocks[j].isEmpty()) {
            anyWagon = true;
            break;
        }
    }

    if (!anyWagon) {
        std::cout << "No wagons to assemble for " << destinationToString(dest) << std::endl;
        return nullptr;
    }

    //  
    struct BlockInfo
    {
        int cargoIdx;
        int heaviest;
    };

    BlockInfo normalBlocks[NUM_CARGOTYPES_INT]; // Array to hold block info
    int blockCount = 0;
    WagonList hazardousBlock; // For hazardous cargo type

    // Transverse all cargo blocks for the destination
    for (int j = 0; j < NUM_CARGOTYPES_INT; ++j)
    {
        if (blocks[j].isEmpty())
            continue;

        CargoType ct = static_cast<CargoType>(j);

        // Collect hazardous wagons seperately
        if (ct == CargoType::HAZARDOUS)
        {
            hazardousBlock.appendList(std::move(blocks[j]));
            continue;
        }

        // Record the heaviest wagon in tblock
        Wagon *front = blocks[j].getFront();
        int maxW = 0;
        if (front)
            maxW = front -> getWeight();

        normalBlocks[blockCount].cargoIdx = j;
        normalBlocks[blockCount].heaviest = maxW;
        blockCount++;

    }

    // Sort blocks by descending order of heaviest wagon
    for (int i = 1; i < blockCount; i++)

    {
        BlockInfo key = normalBlocks[i];
        int j = i - 1;
        while (j >= 0 && normalBlocks[j].heaviest < key.heaviest)
        {
            normalBlocks[j + 1] = normalBlocks[j];
            j--;
        }
        normalBlocks[j + 1] = key;
    }

    // Create a new train and attach blocks in sorted order
    Train *train = new Train(trainName, dest);

    // Attach each non-hazardous cargo block in sorted order
    for (int i = 0; i < blockCount; i++)
    {
        train -> appendWagonList(blocks[normalBlocks[i].cargoIdx]);
    }

    if (!hazardousBlock.isEmpty())
    {
        train -> appendWagonList(hazardousBlock);
    }

    std::cout << "Train " << train -> getName() << " assembled with " << train -> getWagons() << " wagons." << std::endl;

    return nullptr;
}

// Checks whether the entire yard has no wagons. the yard is empty if every destination-cargo list is empty
bool ClassificationYard::isEmpty() const
{

    for (int i = 0; i < NUM_DESTINATIONS_INT; ++i)
    {
        for (int j = 0; j < NUM_CARGOTYPES_INT; ++j)
        {
            if (!blockTrains[i][j].isEmpty())
                return false;
        }
    }

    return true;

}

// Clears all wagons from every block in the yard. 
void ClassificationYard::clear()
{
    for (int i = 0; i < NUM_DESTINATIONS_INT; ++i)
    {
        for (int j = 0; j < NUM_CARGOTYPES_INT; ++j)
        {
            blockTrains[i][j].clear();
        }
    }
}


void ClassificationYard::print() const
{
    for (int i = 0; i < static_cast<int>(Destination::NUM_DESTINATIONS); ++i)
    {
        auto dest = destinationToString(static_cast<Destination>(i));
        std::cout << "Destination " << dest << ":\n";
        for (int j = 0; j < static_cast<int>(CargoType::NUM_CARGOTYPES); ++j)
        {
            if (!blockTrains[i][j].isEmpty())
            {
                auto type = cargoTypeToString(static_cast<CargoType>(j));
                std::cout << "  CargoType " << type << ": ";
                blockTrains[i][j].print();
            }
        }
    }
}