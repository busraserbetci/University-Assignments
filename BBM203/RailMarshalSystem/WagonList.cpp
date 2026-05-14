#include "WagonList.h"

#include <iostream>

WagonList::~WagonList() { clear(); }

// Deletes all wagons from the list and reset pointers
void WagonList::clear()
{

    Wagon *cur = front;
    while (cur)
    {
        Wagon *next = cur -> getNext();
        delete cur;
        cur = next;
    }

    front = nullptr;
    rear = nullptr;
    totalWeight = 0;

}

// Transfer ownership of another WagonList's data without copying. The source list is reset to empty (move constructor)
WagonList::WagonList(WagonList &&other) noexcept
{

    front = other.front;
    rear = other.rear;
    totalWeight = other.totalWeight;

    other.front = nullptr;
    other.rear = nullptr;
    other.totalWeight = 0;

}

// same as move constructor, but for assignment. Clear current list, then takes over another list's data
WagonList &WagonList::operator=(WagonList &&other) noexcept
{
    
    if (this == &other)
        return *this;

    clear();

    front = other.front;
    rear = other.rear;
    totalWeight = other.totalWeight;

    other.front = nullptr;
    other.rear = nullptr;
    other.totalWeight = 0;

    return *this;
}

// Finds a wagon by its ID and returns a pointer to it, return nullptr if not found ID
Wagon *WagonList::findById(int id)
{

    Wagon *cur = front;

    while (cur)
    {
        if (cur -> getID() == id)
            return cur;
        cur = cur -> getNext();
    }
    return nullptr;
}

// Adds a wagon at the end of the doubly-linked list. Updates rear pointer and total weight. 
void WagonList::addWagonToRear(Wagon *w)
{
    if (!w)
        return;

    w -> setNext(nullptr);
    w -> setPrev(nullptr);

    if (isEmpty())
    {
        front = rear = w;
    }
    else
    {
        rear -> setNext(w);
        w -> setPrev(rear);
        rear = w;
    }
    totalWeight += w -> getWeight();
}

int WagonList::getTotalWeight() const { return totalWeight; }

// Returns true if the list is empty.
bool WagonList::isEmpty() const
{
    if (front == nullptr)
        return true;
    return false;
}

// Inserts a wagon in descending order by weight. Keeps the list sorted automatically when inserting. 
void WagonList::insertSorted(Wagon *wagon)
{
    if (!wagon)
        return;

    
    wagon -> setNext(nullptr);
    wagon -> setPrev(nullptr);

    if (isEmpty())
    {
        front = rear = wagon;
        totalWeight += wagon -> getWeight();
        return;
    }

    int w = wagon -> getWeight();

    // Insert at front (heaviest)
    if (w >= front -> getWeight())
    {
        wagon -> setNext(front);
        front -> setPrev(wagon);
        front = wagon;
        totalWeight += wagon -> getWeight();
        return;
    }

    // Insert at end (lightest)
    if (w <= rear -> getWeight())
    {
        rear -> setNext(wagon);
        wagon -> setPrev(rear);
        rear = wagon;
        totalWeight += wagon -> getWeight();
        return;
    }

    // Insert in the middle
    Wagon *cur = front->getNext();
    while (cur)
    {
        if (w >= cur -> getWeight())
        {
            
            Wagon *prev = cur -> getPrev();
            prev -> setNext(wagon);
            wagon -> setPrev(prev);
            wagon -> setNext(cur);
            cur -> setPrev(wagon);
            totalWeight += wagon -> getWeight();
            return;
        }
        cur = cur -> getNext();
    }


    rear -> setNext(wagon);
    wagon -> setPrev(rear);
    rear = wagon;
    totalWeight += wagon -> getWeight();
}

// Appends another WagonList to the end of this one. The source list is cleared after transfer.
void WagonList::appendList(WagonList &&other)
{
   if (other.isEmpty())
        return;

    if (isEmpty())
    {
        front = other.front;
        rear = other.rear;
        totalWeight = other.totalWeight;
    }
    else
    {
        rear -> setNext(other.front);
        other.front -> setPrev(rear);
        rear = other.rear;
        totalWeight += other.totalWeight;
    }

    // Clear the other list
    other.front = nullptr;
    other.rear = nullptr;
    other.totalWeight = 0;
}

// Removes a wagon with the given ID from the list and returns it, not deletion,
Wagon *WagonList::detachById(int id)
{
   Wagon *toRemove = findById(id);
    if (!toRemove)
        return nullptr;

    std::cout << "Wagon " << toRemove -> getID() << " detached from Wagon List. " << std::endl;

    Wagon *prev = toRemove -> getPrev();
    Wagon *next = toRemove -> getNext();

    if (prev)
        prev -> setNext(next);
    else
        front = next;
    if (next)
        next -> setPrev(prev);
    else
        rear = prev; 

    // Disconnect wagon from list
    toRemove -> setNext(nullptr);
    toRemove -> setPrev(nullptr);

    totalWeight -= toRemove -> getWeight();

    return toRemove;
}

// Splits the list starting from the wagon with given ID. returns a new WagonList containing the second half. 
WagonList WagonList::splitAtById(int id)
{
    WagonList newList;

    Wagon *node = findById(id);
    if (!node)
        return newList;


    newList.front = node;
    newList.rear = rear;

    int splitWeight = 0;
    Wagon *cur = node;

    // Calculate total weight of the new list
    while (cur)
    {
        splitWeight += cur -> getWeight();
        cur = cur -> getNext();
    }

    newList.totalWeight = splitWeight;

    // Update current list
    Wagon *prev = node -> getPrev();

    if (prev)
    {
        prev -> setNext(nullptr);
        rear = prev;
    }
    else
    {
    
        front = nullptr;
        rear = nullptr;
    }

    
    node -> setPrev(nullptr);

    
    totalWeight -= splitWeight;

    return newList;
}


void WagonList::print() const
{

    std::cout << *this << std::endl;
    return;
}


std::ostream &operator<<(std::ostream &os, const WagonList &list)
{
    if (list.isEmpty())
        return os;

    Wagon *current = list.front;

    while (current)
    {
        os << "W" << current->getID() << "(" << current->getWeight() << "ton)";
        if (current->getNext())
            os << " - ";
        current = current->getNext();
    }
    return os;
}
