/*
 * Beautiful Capi generates beautiful C API wrappers for your C++ classes
 * Copyright (C) 2015 Petr Petrovich Petrov
 *
 * This file is part of Beautiful Capi.
 *
 * Beautiful Capi is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Beautiful Capi is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Beautiful Capi.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

#include <iostream>
#include "PrinterImpl.h"

// By default newly created objects implies to have value 1 of reference counter
Example::PrinterImpl::PrinterImpl() : mRefCount(1)
{
    std::cout << "Printer ctor" << std::endl;
}

Example::PrinterImpl::~PrinterImpl()
{
    std::cout << "Printer dtor" << std::endl;
}

void Example::PrinterImpl::AddRef()
{
    if (this)
    {
        ++mRefCount;
    }
}

void Example::PrinterImpl::Release()
{
    if (this)
    {
        --mRefCount;
        if (mRefCount <= 0)
        {
            delete this;
        }
    }
}

void Example::PrinterImpl::Show(const char* text) const
{
    std::cout << "print text: " << text << std::endl;
}
