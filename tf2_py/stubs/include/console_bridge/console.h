#pragma once

#include <cstdio>

#define CONSOLE_BRIDGE_logInfo(fmt,...) std::fprintf(stderr, fmt, __VA_ARGS__)
#define CONSOLE_BRIDGE_logWarn(fmt,...) std::fprintf(stderr, fmt, __VA_ARGS__)
#define CONSOLE_BRIDGE_logError(fmt,...) std::fprintf(stderr, fmt, __VA_ARGS__)
