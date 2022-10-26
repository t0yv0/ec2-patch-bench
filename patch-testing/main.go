package main

import (
	"bytes"
	"fmt"

	"github.com/google/uuid"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi/config"
)

func main() {
	pulumi.Run(func(ctx *pulumi.Context) error {
		conf := config.New(ctx, "")
		resourceCount := conf.RequireInt("resource_count")
		resourcePayloadBytes := conf.RequireInt("resource_payload_bytes")

		for i := 0; i < resourceCount; i++ {
			deadweight := generateDeadweight(resourcePayloadBytes)

			dummy, err := NewDummy(ctx, fmt.Sprintf("dummy-%d", i), &DummyArgs{
				Deadweight: pulumi.String(deadweight),
			})
			if err != nil {
				return err
			}

			if i == 0 {
				ctx.Export("ResourcePayloadBytes", dummy.Deadweight.ApplyT(func(x string) int {
					return len(x)
				}))
			}
		}

		ctx.Export("ResourceCount", pulumi.Int(resourceCount))
		return nil
	})
}

func generateDeadweight(size int) string {
	var buf bytes.Buffer
	for buf.Len() < size {
		buf.WriteString(uuid.New().String())
	}
	return buf.String()[0:size]
}
