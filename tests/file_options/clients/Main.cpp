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

#if defined(_WIN32) && defined(_DEBUG)
#include <crtdbg.h>
#endif
#include <iostream>
#include <cstdlib>
#if test00
#include "Example/Geometry/Brep/Body.h"
#elif test01
#include "Example/Geometry/Brep/Body.h"
#elif test02
#include "Body.h"
#elif test03
#include "Body.h"
#elif test04
#include "Example/Geometry/Brep.h"
#elif test05
#include "Example/Geometry/Brep/Brep.h"
#elif test06
#include "Brep.h"
#elif test07
#include "Brep.h"
#elif test08
#include "ExampleOneHeader.h"
#elif test09
#include "Example/Example_forwards.h"
#include "Example/Example_c_api.h"
#include "Example/Geometry/Brep/Body.h"
#endif


void f1(Example::Geometry::Brep::Body body)
{
    std::cout << "Name: " << body.GetName() << std::endl;
    body.SetName("modified name in object copy");
    std::cout << "Name: " << body.GetName() << std::endl;
}

Example::Geometry::Brep::Body create_body()
{
    Example::Geometry::Brep::Body new_body;
    new_body.SetName("new body");
    return new_body;
}

int main()
{
#if defined(_WIN32) && defined(_DEBUG)
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif
    Example::Geometry::Brep::Body body = create_body();
    body.SetName("new name");
    f1(body);
    std::cout << "Name: " << body.GetName() << std::endl;

    return EXIT_SUCCESS;
}
