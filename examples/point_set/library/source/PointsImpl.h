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

#ifndef BEAUTIFUL_CAPI_POINT_SET_POINTS_H
#define BEAUTIFUL_CAPI_POINT_SET_POINTS_H

#include "PositionImpl.h"
#include <vector>

namespace PointSet
{
    class PointsImpl
    {
        std::vector<PositionImpl> mPoints;
        int mRefCount;

    public:
        PointsImpl() : mRefCount(1) {}

        size_t Size() { return mPoints.size(); }
        void Reserve(size_t capacity) { mPoints.reserve(capacity); }
        void Resize(size_t size, PositionImpl* default_value) { mPoints.resize(size, *default_value); }

        PositionImpl* GetElement(size_t index) { return &mPoints[index]; }
        void SetElement(size_t index, PositionImpl* value) { mPoints[index] = *value; }
        void PushBack(PositionImpl* value) { mPoints.push_back(*value); }

        void Clear() { mPoints.clear(); }

        void AddRef() { if (this) ++mRefCount; }
        void Release()
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
    };

    inline void intrusive_ptr_add_ref(PointsImpl* printer)
    {
        printer->AddRef();
    }

    inline void intrusive_ptr_release(PointsImpl* printer)
    {
        printer->Release();
    }
}

#endif /* BEAUTIFUL_CAPI_POINT_SET_POINTS_H */
