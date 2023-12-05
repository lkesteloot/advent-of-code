
from itertools import chain

lines = open("input-5.txt").read().splitlines()

class Span:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def __repr__(self):
        return "[%d,%d)" % (self.begin, self.end)

class Mapping:
    def __init__(self):
        self.maps = []

    def add_map(self, mmap):
        self.maps.append(mmap)

    def prepare(self):
        self.maps.sort(key=lambda mmap: mmap[0].begin)

    def map_span(self, span):
        for src_span, dst_span in self.maps:
            # Before
            begin = min(span.begin, src_span.begin)
            end = min(span.end, src_span.begin)
            if begin < end:
                yield Span(begin, end)
                span = Span(end, span.end)

            # Inside
            begin = max(span.begin, src_span.begin)
            end = min(span.end, src_span.end)
            if begin < end:
                yield Span(
                    dst_span.begin + begin - src_span.begin,
                    dst_span.end + end - src_span.end)
                span = Span(end, span.end)

            if span.begin >= span.end:
                break

        # After
        if span.begin < span.end:
            yield span

mappings = []
mapping = None
for line_number, line in enumerate(lines):
    if line.startswith("seeds: "):
        seeds = list(map(int, line[7:].split()))
        seed_spans = [Span(start, start + length) for start, length in zip(seeds[::2], seeds[1::2])]
    elif line.endswith(":"):
        mapping = Mapping()
        mappings.append(mapping)
    elif line == "":
        pass
    elif mapping is None:
        print("no mapping on line", line_number)
    else:
        dst, src, length = map(int, line.split())
        mapping.add_map( (Span(src, src + length), Span(dst, dst + length)) )

spans = seed_spans
for mapping in mappings:
    mapping.prepare()
    spans = chain.from_iterable(map(mapping.map_span, spans))

print(sorted(spans, key=lambda span: span.begin)[0].begin)

