package com.psiim.psiimserver

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class PsiimServerApplication

fun main(args: Array<String>) {
    runApplication<PsiimServerApplication>(*args)
}
