/*
 * File:    static_deque.cc
 * Author:  Gio
 *
 * Date:    05/21/2013
 */

#ifndef __STATIC_DEQUE_CC__
#define __STATIC_DEQUE_CC__

#include "static_deque.hh"
#include <stdexcept>

#define WRAP_INCR(i, s) (((i) == ((s) - 1)) ? 0 : ((i) + 1))
#define WRAP_DECR(i, s) (((i) == 0) ? ((s) - 1) : ((i) - 1))
#define WRAP_RACC(f, i, s) \
  ((((f) - (i) - 1) < 0) ? ((s) - ((i) - (f)) - 1) : ((f) - (i) - 1))

template<typename T>
StaticDeque<T>::StaticDeque(int static_size) {
  if (static_size <= 0)
    throw std::runtime_error("Cannot instantiate deque to a non-positive size.");
  
  length = static_size;
  data = new T[static_size];
  elems = 0;
  first = 0;
  last = 0;
}

template<typename T>
StaticDeque<T>::StaticDeque(const StaticDeque<T>& orig) {
  length = orig.length;
  data = new T[length];
  elems = orig.elems;
  first = orig.first;
  last = orig.last;
  for (int i = 0; i < orig.length; i++)
    data[i] = orig.data[i];
}

template<typename T>
StaticDeque<T>::~StaticDeque() {
  delete[] data;
}

template<typename T>
int StaticDeque<T>::size() const {
  return elems;
}

template<typename T>
bool StaticDeque<T>::empty() const {
  return elems == 0;
}

template<typename T>
bool StaticDeque<T>::full() const {
  return elems == length;
}

template<typename T>
bool StaticDeque<T>::contains(const T &elem) const {
  for (int i = last; i != first; i = WRAP_INCR(i, length))
    if (data[i] == elem) return true;
  return false;
}

template<typename T>
T& StaticDeque<T>::front() const {
  if (elems > 0) return data[WRAP_DECR(first, length)];
  else throw std::runtime_error("Attempted to access element in empty deque.");
}

template<typename T>
T& StaticDeque<T>::back() const {
  if (elems > 0) return data[last];
  else throw std::runtime_error("Attempted to access element in empty deque.");
}

template<typename T>
T& StaticDeque<T>::pop_front() {
  if (elems > 0) {
    first = WRAP_DECR(first, length);
    T& elem = data[first];
    elems--;
    return elem;
  }
  else throw std::runtime_error("Attempted to remove element in empty deque.");
}

template<typename T>
T& StaticDeque<T>::pop_back() {
  if (elems > 0) {
    T& elem = data[last];
    last = WRAP_INCR(last, length);
    elems--;
    return elem;
  }
  else throw std::runtime_error("Attempted to remove element in empty deque.");
}

template<typename T>
void StaticDeque<T>::push_front(const T& elem) {
  if (elems < length) {
    data[first] = elem;
    first = WRAP_INCR(first, length);
    elems++;
  }
  else throw std::runtime_error("Attempted to add element to full deque.");
}

template<typename T>
void StaticDeque<T>::push_back(const T& elem) {
  if (elems < length) {
    last = WRAP_DECR(last, length);
    data[last] = elem;
    elems++;
  }
  else throw std::runtime_error("Attempted to add element to full deque.");
}

template<typename T>
void StaticDeque<T>::clear() {
  elems = 0;
  first = 0;
  last = 0;
}

template<typename T>
T& StaticDeque<T>::operator[](int index) {
  if (index >= 0 && index < elems) return data[WRAP_RACC(first, index, length)];
  else throw std::runtime_error("Attempted to retrieve non-existant element.");
}

#endif /*__STATIC_DEQUE_CC__*/
