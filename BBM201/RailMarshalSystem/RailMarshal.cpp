#include "RailMarshal.h"
#include <iostream>
#include <sstream>
#include <algorithm>

RailMarshal::RailMarshal()
{
    for (int i = 0; i < NUM_DESTINATIONS_INT; ++i)
    {
        departureYard[i] = TrainTrack(static_cast<Destination>(i));
    }
}

RailMarshal::~RailMarshal()
{
    classificationYard.clear();
    for (int i = 0; i < NUM_DESTINATIONS_INT; ++i)
    {
        while (!departureYard[i].isEmpty())
        {
            Train *t = departureYard[i].departTrain();
            delete t;
        }
    }
}


ClassificationYard &RailMarshal::getClassificationYard()
{
    return classificationYard;
}


TrainTrack &RailMarshal::getDepartureYard(Destination dest)
{
    int idx = static_cast<int>(dest);
    return departureYard[idx];
}

void RailMarshal::processCommand(const std::string &line)
{
    std::istringstream iss(line);
    std::string cmd;
    iss >> cmd;

    if (cmd == "ADD_WAGON")
    {
        int id, weight, maxCoupler;
        std::string cargoStr, destStr;
        if (!(iss >> id >> cargoStr >> destStr >> weight >> maxCoupler))
        {
            std::cout << "Error: Invalid ADD_WAGON parameters.\n";
            return;
        }

        CargoType cargo = parseCargo(cargoStr);
        Destination dest = parseDestination(destStr);

        Wagon *w = new Wagon(id, cargo, dest, weight, maxCoupler);
        classificationYard.insertWagon(w);
        std::cout << "Wagon " << *w << " added to yard." << std::endl;
    }

    else if (cmd == "REMOVE_WAGON")
    {
        int id;
        if (!(iss >> id))
        {
            std::cout << "Error: Invalid REMOVE_WAGON parameters.\n";
            return;
        }

        bool removed = false;
        for (int i = 0; i < NUM_DESTINATIONS_INT && !removed; ++i)
        {
            for (int j = 0; j < NUM_CARGOTYPES_INT && !removed; ++j)
            {
                Wagon *w = classificationYard.getBlockTrain(i, j).detachById(id);
                if (w)
                {
                    std::cout << "Wagon " << id << " removed." << std::endl;
                    delete w;
                    removed = true;
                }
            }
        }
        if (!removed)
            std::cout << "Error: Wagon " << id << " not found." << std::endl;
    }

    else if (cmd == "ASSEMBLE_TRAIN")
    {
        std::string destStr;
        if (!(iss >> destStr))
        {
            std::cout << "Error: Invalid ASSEMBLE_TRAIN parameters.\n";
            return;
        }

        Destination dest = parseDestination(destStr);
        std::string trainName = departureYard[static_cast<int>(dest)].generateTrainName();
        Train *t = classificationYard.assembleTrain(dest, trainName);

        if (!t)
            return;

        int splitCounter = 1;
        Train *split = t->verifyCouplersAndSplit(splitCounter);
        while (split)
        {
            ++splitCounter;
            departureYard[static_cast<int>(dest)].addTrain(split);
            split = t->verifyCouplersAndSplit(splitCounter);
        }

        departureYard[static_cast<int>(dest)].addTrain(t);
    }

    else if (cmd == "DISPATCH_TRAIN")
    {
        std::string destStr;
        if (!(iss >> destStr))
        {
            std::cout << "Error: Invalid DISPATCH parameters.\n";
            return;
        }

        Destination dest = parseDestination(destStr);
        TrainTrack &track = departureYard[static_cast<int>(dest)];

        if (track.isEmpty())
        {
            std::cout << "Error: No trains to dispatch from track " << destStr << ".\n";
            return;
        }

        Train *t = track.departTrain();
        if (t)
        {
            std::cout << "Dispatching " << t->getName() << " (" << t->getTotalWeight() << " tons)." << std::endl;
            delete t;
        }
    }

    else if (cmd == "PRINT_YARD")
    {
        std::cout << "--- classification Yard ---\n";
        classificationYard.print();
    }

    else if (cmd == "PRINT_TRACK")
    {
        std::string destStr;
        if (!(iss >> destStr))
        {
            std::cout << "Error: Invalid PRINT_TRACK parameters.\n";
            return;
        }

        Destination dest = parseDestination(destStr);
        departureYard[static_cast<int>(dest)].printTrack();
    }

    else if (cmd == "AUTO_DISPATCH")
    {
        std::string mode;
        if (!(iss >> mode))
        {
            std::cout << "Error: Invalid AUTO_DISPATCH parameters.\n";
            return;
        }

        std::string up = toUpper(mode);
        if (up == "ON")
        {
            TrainTrack::autoDispatch = true;
            std::cout << "Auto dispatch enabled" << std::endl;
        }
        else if (up == "OFF")
        {
            TrainTrack::autoDispatch = false;
            std::cout << "Auto dispatch disabled" << std::endl;
        }
        else
        {
            std::cout << "Error: Invalid AUTO_DISPATCH parameters.\n";
        }
    }

    else if (cmd == "CLEAR")
    {
        classificationYard.clear();
        for (int i = 0; i < NUM_DESTINATIONS_INT; ++i)
        {
            while (!departureYard[i].isEmpty())
            {
                Train *t = departureYard[i].departTrain();
                delete t;
            }
        }
        std::cout << "System cleared." << std::endl;
    }

    else
    {
        std::cout << "Error: Unknown command '" << cmd << "'" << std::endl;
    }
}

void RailMarshal::dispatchFromTrack(Destination track)
{

    TrainTrack &t = departureYard[static_cast<int>(track)];

    if (t.isEmpty())
    {
        std::cout << "Error: No trains to dispatch from Track " << static_cast<int>(track) << ".\n";
        return;
    }

    Train *departed = t.departTrain();
    if (departed)
    {
        std::cout << "Train " << departed->getName() << " departed from Track " << static_cast<int>(track) << " (" << destinationToString(track) << ").\n";
        delete departed;
    }

}

void RailMarshal::printDepartureYard() const
{
    for (int i = 0; i < NUM_DESTINATIONS_INT; ++i)
    {
        std::cout << "Track " << i << " ("
                  << destinationToString(static_cast<Destination>(i)) << "):\n";
        departureYard[i].printTrack();
    }
}


void RailMarshal::printStatus() const
{
    std::cout << "--- classification Yard ---\n";
    classificationYard.print();

    std::cout << "--- Departure Yard ---\n";
    for (int i = 0; i < static_cast<int>(Destination::NUM_DESTINATIONS); ++i)
    {
        departureYard[i].printTrack();
    }
}
