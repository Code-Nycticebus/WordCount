#define CEBUS_IMPLEMENTATION
#include "cebus.h"

typedef struct {
  Str word;
  usize count;
} Occurences;

CmpOrdering cmp(const void *a, const void *b) {
  return ((const Occurences *)b)->count - ((const Occurences *)a)->count;
}

int main(int argc, const char **argv) {
  Str filename = argc < 2 ? STR(__FILE__) : str_from_cstr(argv[1]);

  Arena arena = {0};
  Error error = {0};
  Str content = file_read_str(filename, &arena, &error);
  error_context(&error, {
    cebus_log_error(STR_FMT, STR_ARG(error_msg()));
    return -1;
  });

  HashMap *map = hm_create(&arena);
  DA(Occurences) occurences;
  da_init(&occurences, &arena);

  for (Str word = {0};
       str_try_chop_by_predicate(&content, c_is_space, &word);) {
    u64 hash = str_hash(word);
    const usize *idx = hm_get_usize(map, hash);
    if (idx == NULL) {
      hm_insert_usize(map, hash, da_len(&occurences));
      da_push(&occurences, (Occurences){.word = word, .count = 1});
    } else {
      da_get(&occurences, *idx).count++;
    }
  }

  da_sort(&occurences, &occurences, cmp);

  for (usize i = 0; i < 3; i++) {
    Occurences *o = &da_get(&occurences, i);
    cebus_log("%" USIZE_FMT ": " STR_FMT ": %" USIZE_FMT, i + 1,
              STR_ARG(o->word), o->count);
  }

  arena_free(&arena);
}
