# BMessage

## Data Members

:::{section}
---
members:
 - uint32 BMessage::what
---

A coded constant that captures what the message is about.
:::

## Member Functions

:::{section}
---
functions:
 - status_t BMessage::GetCurrentSpecifier(int32* index, BMessage* specifier = NULL,
        int32* what = NULL, const char** property = NULL) const
 - status_t BMessage::PopSpecifier()
---

`GetCurrentSpecifier()` unpacks the current specifier in the `BMessage`, the one at the top of the
specifier stack; `PopSpecifer()` changes the notion of which specifier is current, by popping the
current one from the stack.

These functions aid in implementing a class-specific version of {cpp:class}`BHandler`'s
{cpp:func}`~BHandler::ResolveSpecifier()` function---the first gets the specifier that needs to be
resolved, and the second pops it from the stack....
:::

```{cpp:function} status_t BMessage::AddData(const char* name, type_code type, const void* data, ssize_t numBytes, bool fixedSize = true, int32 numItems = 1)
```
:::{code} cpp
status_t AddData(const char* name,
                type_code type,
                const void* data,
                ssize_t numBytes,
                bool fixedSize = true,
                int32 numItems = 1);
:::
```{cpp:function} status_t BMessage::BMessage::AddBool(const char* name, bool aBool)
```
:::{code} cpp
status_t AddBool(const char* name, bool aBool);
:::
```{cpp:function} BMessage::AddInt8()
```
:::{code} cpp
status_t AddInt8(const char* name, int8 anInt8);
:::
```{cpp:function} BMessage::AddInt16()
```
:::{code} cpp
status_t AddInt16(const char* name, int16 anInt16);
:::
```{cpp:function} BMessage::AddInt32()
```
:::{code} cpp
status_t AddInt32(const char* name, int32 anInt32);
:::
```{cpp:function} BMessage::AddInt64()
```
:::{code} cpp
status_t AddInt64(const char* name, int64 anInt64);
:::
```{cpp:function} BMessage::AddFloat()
```
:::{code} cpp
status_t AddFloat(const char* name, float anloat);
:::
```{cpp:function} BMessage::AddDouble()
```
:::{code} cpp
status_t AddDouble(const char* name, double aDouble);
:::
```{cpp:function} BMessage::AddString()
```
:::{code} cpp
status_t AddString(const char* name, const char *string);
status_t AddString(const char* name, const BString string);
:::
```{cpp:function} BMessage::AddPoint()
```
:::{code} cpp
status_t AddPoint(const char* name, BPoint point);
:::
```{cpp:function} BMessage::AddRect()
```
:::{code} cpp
status_t AddRect(const char* name, BRect rect);
:::
```{cpp:function} BMessage::AddRef()
```
:::{code} cpp
status_t AddRef(const char* name, const entry_ref* ref);
:::
```{cpp:function} BMessage::AddMessage()
```
:::{code} cpp
status_t AddMessage(const char* name, const BMessage* message);
:::
```{cpp:function} BMessage::AddMessenger()
```
:::{code} cpp
status_t AddMessenger(const char* name, BMessenger messenger);
:::
```{cpp:function} BMessage::AddPointer()
```
:::{code} cpp
status_t AddPointer(const char* name, const void* pointer);
:::
```{cpp:function} BMessage::AddFlat()
```
:::{code} cpp
status_t AddFlat(const char* name, BFlattenable* object, int32 numItems = 1);
:::

These functions add data to the field named `name` and assign a data type to the field. Field names
can be no longer than 255 characters. If more than one item of data is added under the same name,
the `BMessage` creates an array of data for that name. Each time you add another value (to the same
name), the value is added to the end of the array---you can't add a value at a specific index. A
given field can only store one type of data.

`AddData()` copies `numBytes` of `data` into the field, and assigns the data a `type` code. It
copies whatever the `data` pointer points to. For example, if you want to add a string of characters
to the message, `data` should be the string pointer (`char*`). If you want to add only the string
pointer, not the characters themselves, `data` should be a pointer to the pointer (`char**`). The
assigned `type` must be a specific data type; it should not be {cpp:enum}`B_ANY_TYPE`.

When you call `AddData()` to place the first item in an array under a new name, you can provide it
with two arguments, `fixedSize` and `numItems`, that will improve the object's efficiency. If the
`fixedSize` flag is {cpp:expr}`true`, each item in the array must have the same number of bytes; if
the flag is {cpp:expr}`false`, items can vary in size. `numItems` tells the object to pre-allocate
storage for some number of items. This isn't a limit, you can add more than `numItems` to the field.

Most of the other functions are variants of `AddData()` that hard-code the field's type. For
example, `AddFloat()` assigns the type {cpp:enum}`B_FLOAT_TYPE`; `AddBool()` assigns
{cpp:enum}`B_BOOL_TYPE`, and so on.

`AddString()`, like `AddData()`, takes a pointer to the data it adds, or you can use a
{cpp:class}`BString` object. The `string` must be null-terminated; the null character is counted and
copied into the message. Similarly, `AddRef()` adds the pointed to `entry_ref` structure to the
message (and the variable-length name that's one of the elements of the structure); `AddMessage()`
adds one `BMessage` to another.

The other functions are simply passed the data directly. For example, `AddInt32()` takes an int32 or
uint32 and `AddMessenger()` takes a {cpp:class}`BMessenger` object, whereas `AddData()` would be
passed a pointer to an int32 and a pointer to a {cpp:class}`BMessenger`. `AddPointer()` adds only
the pointer it's passed, not the data it points to. To accomplish the same thing, `AddData()` would
take a pointer to the pointer. (The pointer will be valid only locally; it won't be useful to a
remote destination.)

`AddFlat()` flattens an `object` (by calling its `Flatten()` function) and adds the flat data to the
message. It calls the object's {cpp:func}`~BFlattenable::TypeCode()` function to learn the type code
it should associated with the data. Objects that are added through `AddFlat()` must inherit from
{cpp:class}`BFlattenable` (defined in the "Support Kit").

You can also provide a `numItems` hint to `AddFlat()` when you call it to set up a new array.
`AddFlat()` calls the object's {cpp:func}`~BFlattenable::IsFixedSize()` function to discover whether
all items in the array will be the same size.

The functions return a {cpp:enum}`B_ERROR` if the data is too massive to be added to the message,
{cpp:enum}`B_BAD_TYPE` if the data can't be added to an existing array because it's the wrong type,
{cpp:enum}`B_NO_MEMORY` if the `BMessage` can't get enough memory to hold the data, and
{cpp:enum}`B_BAD_VALUE` if the proposed `name` for the data is longer than 255 bytes. If all goes
well, they return {cpp:enum}`B_OK`.

There's no limit on the number of named fields a message can contain, or on the size a field's data.
However, since the serach is linear, combing through a very long list of names to find a particular
piece of data my be inefficient. Also, because of the amount of data that must be moved, an
extremely large message can slow the delivery mechanism. It's sometimes better to put some of the
information in a common location (a file, a private clipboard, a shared area of memory) and just
refer to it in the message.

See also: {cpp:func}`~BMessage::FindData()`, {cpp:func}`~BMessage::GetInfo()`

