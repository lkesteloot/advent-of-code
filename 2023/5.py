
lines = [line.strip() for line in open("input-5.txt")]

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
        out_spans = []

        for src_span, dst_span in self.maps:
            # Before
            begin = min(span.begin, src_span.begin)
            end = min(span.end, src_span.begin)
            if begin < end:
                out_spans.append(Span(begin, end))
                span = Span(end, span.end)

            # Inside
            begin = max(span.begin, src_span.begin)
            end = min(span.end, src_span.end)
            if begin < end:
                out_spans.append(Span(
                    dst_span.begin + begin - src_span.begin,
                    dst_span.end + end - src_span.end))
                span = Span(end, span.end)

            if span.begin >= span.end:
                break

        # After
        if span.begin < span.end:
            out_spans.append(span)

        return out_spans

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

for mapping in mappings:
    mapping.prepare()

spans = seed_spans
for mapping in mappings:
    out_spans = []
    for span in spans:
        out_spans.extend(mapping.map_span(span))
    spans = out_spans
spans.sort(key=lambda span: span.begin)
print(spans[0].begin)

