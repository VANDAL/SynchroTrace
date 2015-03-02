/*
 * File:    static_deque.hh
 * Author:  Gio
 *
 * Date:    05/21/2013
 */

#ifndef __STATIC_DEQUE_HH__
#define __STATIC_DEQUE_HH__

//#include <iostream>

template<typename T>
class StaticDeque {
  public:
    StaticDeque(int static_size);
    StaticDeque(const StaticDeque<T>& orig);
    virtual ~StaticDeque();

    int size() const;
    bool empty() const;
    bool full() const;
    bool contains(const T &elem) const;

    T& front() const;
    T& back() const;

    T& pop_front();
    T& pop_back();

    void push_front(const T &elem);
    void push_back(const T &elem);

    void clear();

    T& operator[](int index);

  private:
    T* data;
    int length, elems, first, last;
};

//template<class U>
//std::ostream& std::operator<<(std::ostream &stream, const StaticDeque<U>& deq);

#include "static_deque.cc"

#endif /*__STATIC_DEQUE_HH__*/
