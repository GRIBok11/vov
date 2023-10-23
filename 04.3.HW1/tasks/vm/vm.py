"""
Simplified VM code which works for some cases.
You need extend/rewrite code to pass all cases.
"""

import builtins
import dis
import types
import typing as tp


class Frame:
    """
    Frame header in cpython with description
        https://github.com/python/cpython/blob/3.11/Include/frameobject.h

    Text description of frame parameters
        https://docs.python.org/3/library/inspect.html?highlight=frame#types-and-members
    """

    def __init__(self,
                 frame_code: types.CodeType,
                 frame_builtins: dict[str, tp.Any],
                 frame_globals: dict[str, tp.Any],
                 frame_locals: dict[str, tp.Any]) -> None:
        self.code = frame_code
        self.i = 0
        self.last_exception: tp.Any = None
        self.block_holder: tp.Any = []
        self.builtins = frame_builtins
        self.globals = frame_globals
        self.locals = frame_locals
        self.data_stack: tp.Any = []
        self.return_value = None

    def top(self) -> tp.Any:
        return self.data_stack[-1]

    def pop(self) -> tp.Any:
        return self.data_stack.pop()

    def push(self, *values: tp.Any) -> None:
        self.data_stack.extend(values)

    def popn(self, n: int) -> tp.Any:
        """
        Pop a number of values from the value stack.
        A list of n values is returned, the deepest value first.
        """
        if n > 0:
            returned = self.data_stack[-n:]
            self.data_stack[-n:] = []
            return returned
        else:
            return []

    def run(self) -> tp.Any:

        ll = []

        for instruction in dis.get_instructions(self.code):
            ll.append(instruction)

        while True:
            if self.i >= len(ll):
                break
            getattr(self, ll[self.i].opname.lower() + "_op")(ll[self.i].argval)
            self.i += 1
        return self.return_value

    def resume_op(self, arg: int) -> tp.Any:
        pass

    def push_null_op(self, arg: int) -> tp.Any:
        pass

    def precall_op(self, arg: int) -> tp.Any:
        pass

    def call_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.11.5/library/dis.html#opcode-CALL
        """
        arguments = self.popn(arg)
        f = self.pop()
        self.push(f(*arguments))

    def load_const_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.11.5/library/dis.html#opcode-LOAD_CONST
        """
        self.push(arg)

    def return_value_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.11.5/library/dis.html#opcode-RETURN_VALUE
        """
        self.return_value = self.pop()

    def pop_top_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.11.5/library/dis.html#opcode-POP_TOP
        """
        self.pop()

    def store_name_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.11.5/library/dis.html#opcode-STORE_NAME
        """
        const = self.pop()
        self.locals[arg] = const

    def store_global_op(self, arg: str) -> None:
        value = self.pop()
        self.globals[arg] = value
        self.locals[arg] = value

    def binary_op_op(self, opcode):
        if len(self.data_stack) < 2:
            raise ValueError
        op2 = self.pop()
        op1 = self.pop()
        result = None

        if opcode == 13 or opcode == 0:
            result = op1 + op2
        elif opcode == 24 or opcode == 11:
            result = op1 / op2
        elif opcode == 1 or opcode == 14:
            result = op1 & op2
        elif opcode == 7 or opcode == 20:
            result = op1 | op2
        elif opcode == 10 or opcode == 23:
            result = op1 - op2
        elif opcode == 5 or opcode == 18:
            result = op1 * op2
        elif opcode == 8 or opcode == 21:
            result = op1 ** op2
        elif opcode == 12 or opcode == 25:
            result = op1 ^ op2
        elif opcode == 6 or opcode == 19:
            result = op1 % op2
        elif opcode == 3 or opcode == 16:
            result = op1 << op2
        elif opcode == 22 or opcode == 9:
            result = op1 >> op2
        elif opcode == 2 or opcode == 15:
            result = op1 // op2
        if result is not None:
            self.push(result)

    def unpack_sequence_op(self, count):
        sequence = self.pop()
        if not isinstance(sequence, (list, tuple)):
            raise TypeError("Argument must be a list or tuple")

        for element in reversed(sequence):
            self.push(element)

    def compare_op_op(self, op):
        if len(self.data_stack) < 2:
            raise ValueError("Not enough values")

        operand2 = self.pop()
        operand1 = self.pop()
        result = None

        if op == '==':
            result = operand1 == operand2
        elif op == '<':
            result = operand1 < operand2
        elif op == '<=':
            result = operand1 <= operand2
        elif op == '>':
            result = operand1 > operand2
        elif op == '>=':
            result = operand1 >= operand2
        elif op == '!=':
            result = operand1 != operand2
        else:
            raise NameError

        self.push(result)

    def pop_jump_forward_if_false_op(self, offset):
        value = self.pop()

        if not value:
            self.i = self.find_wanted_ind_by_offset(offset)

    def find_wanted_ind_by_offset(self, offset):
        for i, instr in enumerate(dis.get_instructions(self.code)):
            if instr.offset == offset:
                return i - 1

    def pop_jump_forward_if_true_op(self, offset):
        value = self.pop()
        if value:
            self.i = self.find_wanted_ind_by_offset(offset)

    def pop_jump_back_if_false_op(self, offset):
        value = self.pop()
        if not value:
            self.i = self.find_wanted_ind_by_offset(offset)

    def jump_backward_op(self, offset):
        self.i = self.find_wanted_ind_by_offset(offset)

    def nop_op(self, arg):
        pass

    def jump_forward_op(self, offset):
        self.i = self.find_wanted_ind_by_offset(offset)

    def pop_jump_backward_if_true_op(self, offset):
        value = self.pop()
        if value:
            self.i = self.find_wanted_ind_by_offset(offset)

    def binary_subscr_op(self, arg):
        op2 = self.pop()
        op1 = self.pop()
        self.push(op1[op2])

    def unary_positive_op(self, arg):
        a = self.pop()
        self.push(+a)

    def unary_negative_op(self, arg):
        a = self.pop()
        self.push(-a)

    def unary_not_op(self, arg):
        a = self.pop()
        self.push(not a)

    def unary_invert_op(self, arg):
        a = self.pop()
        self.push(~a)

    def jump_if_true_or_pop_op(self, offset):
        a = self.pop()
        if a:
            self.i = self.find_wanted_ind_by_offset(offset)
            self.push(a)

    def get_iter_op(self, arg) -> None:
        iterable = self.pop()
        if iterable is not None:
            self.push(iter(iterable))
        else:
            self.push(None)

    def for_iter_op(self, offset: int) -> None:
        iterator = self.top()

        if iterator is not None:
            try:
                item = next(iterator)
                self.push(item)
            except StopIteration:
                self.pop()
                self.i = self.find_wanted_ind_by_offset(offset)
        else:
            self.pop()
            self.i = self.find_wanted_ind_by_offset(offset)

    def build_slice_op(self, n):
        if n == 2:
            end = self.pop()
            start = self.pop()
            self.push(slice(start, end))

        if n == 3:
            step = self.pop()
            end = self.pop()
            start = self.pop()
            self.push(slice(start, end, step))

    def build_list_op(self, size):
        items = [self.pop() for _ in range(size)]
        items.reverse()
        self.push(list(items))

    def build_tuple_op(self, size):
        items = [self.pop() for _ in range(size)]
        items.reverse()
        self.push(tuple(items))

    def list_extend_op(self, arg):
        tmp = list(self.pop())
        ll = self.pop()
        ll.extend(tmp)
        self.push(ll)

    def build_map_op(self, size: int):
        key_value_pairs = []
        for _ in range(size):
            val = self.pop()
            key = self.pop()
            key_value_pairs.append((key, val))
        result_dict = dict(key_value_pairs)
        self.push(result_dict)

    def build_const_key_map_op(self, count):
        keys = self.pop()
        values = [self.pop() for _ in range(count)]
        values.reverse()
        result_dict = dict(zip(keys, values))
        self.push(result_dict)

    def load_assertion_error_op(self, arg):
        self.push(AssertionError)

    def raise_varargs_op(self, argc):
        if argc == 0:
            raise
        elif argc == 1:
            raise self.data_stack[-1]
        elif argc == 2:
            raise self.data_stack[-2] from self.data_stack[-1]

    def load_method_op(self, method_name):

        obj = self.pop()

        if not hasattr(obj, method_name):
            raise AttributeError(f"{type(obj).__name}  has no '{method_name}'")

        method = getattr(obj, method_name)

        self.push(method)

    def swap_op(self, arg: int) -> None:
        v1 = self.pop()
        v2 = self.pop()
        self.push(v1)
        self.push(v2)

    def jump_if_false_or_pop_op(self, offset: int):
        op = self.pop()
        if not op:
            self.i = self.find_wanted_ind_by_offset(offset)
            self.push(op)

    def contains_op_op(self, arg):
        op2 = self.pop()
        op1 = self.pop()

        if arg == 1:
            self.push(op1 not in op2)
        else:
            self.push(op1 in op2)

    def is_op_op(self, arg):
        op2 = self.pop()
        op1 = self.pop()

        if arg == 1:
            self.push(op1 is not op2)
        else:
            self.push(op1 is op2)

    def store_fast_op(self, arg):
        op = self.pop()
        self.locals[arg] = op

    def load_fast_op(self, arg):
        try:
            op = self.locals[arg]
        except KeyError:
            UnboundLocalError
        self.push(op)

    def pop_jump_forward_if_none_op(self, offset):
        value = self.pop()

        if value is None:
            self.i = self.find_wanted_ind_by_offset(offset)

    def build_string_op(self, count):
        s = ""
        ll = []
        for i in range(count):
            ll.append(self.pop())

        for elem in reversed(ll):
            s += elem

        self.push(s)

    def format_value_op(self, flags):

        # value = self.pop()
        # if (flags & 0x03) == 0x00:
        #     pass
        # elif (flags & 0x03) == 0x01:
        #     value = str(value)
        # elif (flags & 0x03) == 0x02:
        #     value = repr(value)
        # elif (flags & 0x03) == 0x03:
        #     value = ascii(value)
        # elif(flags & 0x04) != 0x04:
        #     fmt_spec = ""
        #
        # res = PyObject_Format(value, fmt_spec)

        value = self.pop()
        self.push(str(value))

    def make_function_op(self, arg: int) -> None:
        code = self.pop()

        kw_defaults = self.pop() if arg & 0x08 else {}
        defaults = self.pop() if arg & 0x04 else ()

        def f(*args: tp.Any, **kwargs: tp.Any) -> tp.Any:
            f_locals = {name: value for name, value in
                        zip(code.co_varnames, defaults)}
            num_args = min(code.co_argcount, len(args))
            f_locals.update(zip(code.co_varnames[:num_args], args[:num_args]))

            if len(args) > num_args and code.co_flags & 0x04:
                f_locals[code.co_varnames[code.co_argcount]] = args[num_args:]

            if kwargs and code.co_flags & 0x08:
                f_locals[code.co_varnames[-1]] = kwargs

            for kw, default in kw_defaults.items():
                f_locals.setdefault(kw, default)

            frame = Frame(code, self.builtins, self.globals, f_locals)
            return frame.run()

        self.push(f)

    def build_set_op(self, n):
        ll = []
        for a in range(n):
            tmp = self.pop()
            ll.append(tmp)

        self.push(set(ll))

    def set_update_op(self, i):
        seq = self.pop()
        set.update(self.data_stack[-i], seq)

    def copy_op(self, i):
        assert i > 0
        self.data_stack.append(self.data_stack[-i])

    def store_subscr_op(self, arg):
        key = self.pop()
        container = self.pop()
        value = self.pop()
        container[key] = value

    def delete_subscr_op(self, arg):
        key = self.pop()
        container = self.pop()
        del container[key]

    def delete_name_op(self, arg):
        if arg in self.locals:
            del (self.locals[arg])
        elif arg in self.globals:
            del (self.globals[arg])
        elif arg in self.builtins:
            del (self.builtins[arg])
        else:
            raise NameError

    def delete_global_op(self, arg):
        if arg in self.globals:
            del (self.globals[arg])
        else:
            raise NameError

    def delete_fast_op(self, arg):
        if arg in self.locals:
            del (self.locals[arg])
        else:
            raise NameError

    def list_to_tuple_op(self, arg):
        ll = self.pop()
        self.push(tuple(ll))

    def store_attr_op(self, arg):
        try:
            name_index = self.code.co_names.index(arg)
        except ValueError:
            raise AttributeError

        name = self.code.co_names[name_index]
        op2 = self.pop()
        op1 = self.pop()
        setattr(op2, name, op1)

    def load_attr_op(self, namei):
        attr_name = namei

        obj = self.pop()

        if hasattr(obj, attr_name):
            attr_value = getattr(obj, attr_name)
            self.push(attr_value)
        else:
            raise AttributeError

    def delete_attr_op(self, namei):
        obj = self.pop()
        delattr(obj, namei)

    def load_build_class_op(self, classs):
        self.push(self.builtins['__build_class__'])

    def setup_annotations_op(self, arg):
        if '__annotations__' not in self.locals:
            self.locals['__annotations__'] = {}

    def dict_update_op(self, i):
        map = self.pop()
        dict.update(self.data_stack[-i], map)

    def import_name_op(self, namei):

        module_name = namei
        fromlist = self.pop()
        level = self.pop()

        imported_module = __import__(module_name, globals(),
                                     locals(), fromlist, level)

        self.push(imported_module)

    def import_star_op(self, arg):
        module = self.pop()
        try:
            imported_items = vars(module)
            for name, value in imported_items.items():
                self.locals[name] = value
            self.push(imported_items)
        except Exception:
            raise ImportError()

    def import_from_op(self, namei):
        attr_name = namei
        module = self.top()

        try:
            attr = getattr(module, attr_name)
            self.push(attr)
        except AttributeError:
            raise AttributeError()

    def load_name_op(self, arg: str) -> None:

        if arg in self.locals:
            self.push(self.locals[arg])

        elif arg in self.globals:
            self.push(self.globals[arg])

        elif arg in self.builtins:
            self.push(self.builtins[arg])

        else:
            self.last_exception = NameError(arg)
            self.exception_handling()

    def load_global_op(self, arg: str) -> None:
        if arg in self.locals:
            self.push(self.locals[arg])

        elif arg in self.globals:
            self.push(self.globals[arg])

        elif arg in self.builtins:
            self.push(self.builtins[arg])

        else:
            self.last_exception = NameError(arg)
            self.exception_handling()

    def exception_handling(self):
        if len(self.block_holder) == 0:
            raise self.last_exception

        block_type, handler, level = self.block_holder.pop()
        if block_type == 'EXCEPT':
            self.data_stack = self.data_stack[:level]
            self.data_stack.append(self.last_exception)
            self.last_exception = None
            self.index = handler - 1
        else:
            raise ValueError("Unexpected handler type")

    def setup_except_op(self, delta: int):
        block_type = "EXCEPT"

        handler = delta
        level = len(self.data_stack)
        self.block_holder.append((block_type, handler, level))

    def pop_except_op(self, arg):
        self.check_block_can_be_finished("EXCEPT")
        self.block_holder.pop()

    def end_finally_op(self, arg):
        if self.last_exception:
            self.data_stack.pop()

        self.data_stack.pop()
        self.data_stack.pop()

    def check_block_can_be_finished(self, block_type):
        top = self.block_holder[-1]

        assert top[0] == block_type, f"Expected {block_type} block on stack!"


class VirtualMachine:
    def run(self, code_obj: types.CodeType) -> None:
        """
        :param code_obj: code for interpreting
        """
        globals_context: dict[str, tp.Any] = {}
        frame = Frame(code_obj, builtins.globals()['__builtins__'],
                      globals_context, globals_context)
        return frame.run()
