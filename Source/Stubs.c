#define STUB(SYMBOL)                                       \
    extern __attribute__((section("stubs"))) void SYMBOL() \
    {                                                      \
        __nop();                                           \
        __nop();                                           \
        __nop();                                           \
    } // filled with nops so linker doesnt nop out bl calls to stub functions

// STUB(_ZnajRKSt9nothrow_t)
// STUB(_ZnwjRKSt9nothrow_t)
// STUB(_ZdlPv)

// STUB(_ZTVN10__cxxabiv117__class_type_infoE) // why
// STUB(_ZTVN10__cxxabiv120__si_class_type_infoE)

// STUB(_ZN2nn3srv6detail7Service16GetServiceHandleEPNS_6HandleEPKcij)

// STUB(_ZN2nn3ndm16SuspendSchedulerEb)
// STUB(_ZN2nn3cfg3CTR10InitializeEv)

#undef STUB
