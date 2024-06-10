#include <stdlib.h>
#include "autonomous_trust/structures/map_priv.h"
#include "autonomous_trust/config/protobuf_shutdown.h"
#include "autonomous_trust/utilities/exception.h"
#include "autonomous_trust/utilities/logger.h"

#define DEBUG_TESTS 0

#if DEBUG_TESTS
#define ck_assert_int_eq(x, y)
#define ck_assert_int_ne(x, y)
#define ck_assert_str_eq(x, y)
#define ck_assert_ptr_nonnull(x)
#define ck_assert_ret_ok(x) x
#define ck_assert_ret_nonzero(x) x
#else
#include <check.h>
#define ck_assert_ret_ok(x) ck_assert_int_eq(0, x)
#define ck_assert_ret_nonzero(x) ck_assert_int_ne(0, x)
#endif

#if DEBUG_TESTS
void test_map())
#else
START_TEST(test_map)
#endif
{
    logger_t logger;
    ck_assert_ret_ok(logger_init(&logger, DEBUG, NULL));

    // FIXME
    log_exception(&logger);
}
#if !DEBUG_TESTS
END_TEST

Suite *test_suite(void)
{
    Suite *s = suite_create("Map");
    TCase *tc_core = tcase_create("Core");

    tcase_add_test(tc_core, test_map);
    suite_add_tcase(s, tc_core);

    return s;
}

int main(void)
{
    int number_failed;
    Suite *s = test_suite();
    SRunner *sr = srunner_create(s);

    srunner_run_all(sr, CK_VERBOSE);
    number_failed = srunner_ntests_failed(sr);
    srunner_free(sr);
    return (number_failed == 0) ? EXIT_SUCCESS : EXIT_FAILURE;
}
#else
int main(void)
{
    testMap();
    shutdown_protobuf_library();
    return 0;
}
#endif
